from database import conectar
from temas import listar_temas
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada
import sqlite3 
import re
from datetime import datetime
from colorama import Fore, Style

# registrar
def registrar_material():

    print("\n=== REGISTRAR NOVO MATERIAL ===")
    print(aviso_cancelar())

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        titulo = ler_entrada("\nTítulo: ", str)
        if titulo is None: return

        # valida o tipo 
        tipos_validos = ['artigo', 'audiolivro', 'aula', 'curso', 'documentação', 'ebook', 'exercício', 'livro', 'mentoria', 'podcast', 'projeto', 'repositório', 'roadmap', 'tutorial', 'vídeo']
        
        while True:
            print("\nEscolha o tipo de material:")
            for n, tipo in enumerate(tipos_validos, start=1):
                print(f"{n}. {tipo.capitalize()}")
            
            try:
                escolha_tipo = ler_entrada("\nDigite o número correspondente: ", int)
                if escolha_tipo is None: return
                tipo = tipos_validos[escolha_tipo - 1]
                break
            except (ValueError, IndexError):
                print(f"\n{erro()} Entrada inválida. Escolha um entre 1 e {len(tipos_validos)}.")

        # valida o nivel 
        niveis_validos = ['básico', 'intermediário', 'avançado']
        
        while True:
            print("\nEscolha o nível:")
            for n, niveis in enumerate(niveis_validos, start=1):
                print(f"{n}. {niveis.capitalize()}")

            try:
                escolha_nivel = ler_entrada("\nDigite o número correspondente: ", int)
                if escolha_nivel is None: return
                nivel = niveis_validos[escolha_nivel - 1]
                break
            except (ValueError, IndexError):
                print(f"\n{erro()} Entrada inválida. Escolha um entre 1 e {len(niveis_validos)}.")
            
        # Data (com valor padrão) 
        while True:
            data = ler_entrada("\nData (DD/MM/AAAA ou clique Enter para hoje): ", str)
            if data is None:
                return
            if not data:
                data = datetime.now().strftime("%d/%m/%Y")
                break

            try:
                data_objeto = datetime.strptime(data, "%d/%m/%Y")
                data = data_objeto.strftime("%d/%m/%Y")
                break
            except ValueError:
                print(f"\n{erro()} Formato de data inválido. Use DD/MM/AAAA (ex: 31/12/2025).")


        # Link (obrigatório) 
        padrao_url = re.compile(r'^(https?://)'                  
    r'([a-zA-Z0-9-]+\.)+'            
    r'([a-zA-Z]{2,})'                
    r'(/[^\s]*)?$'  )

        while True:
            link = ler_entrada("\nLink (URL): ", str)
            if link is None: return
            link = link.strip()
            
            if not link:
                print(f"\n{erro()} O link é obrigatório.")
                continue

            
            if not padrao_url.match(link):
                print(f"\n{erro()} Insira uma URL válida (começando com http:// ou https://).")
                continue

            # Verificação no banco
            cursor.execute("SELECT id FROM materiais WHERE link = ?", (link,))
            if cursor.fetchone():
                print(f"\n{erro()} Este link já foi cadastrado. Tente outro.")
                continue
            
            break

        # Palavras-chave
        palavras_chave = ler_entrada("\nPalavras-chave (separadas por vírgula): ", str)
        if palavras_chave is None: return
        
        palavras_chave = palavras_chave.strip()

        if not palavras_chave:
            palavras_chave = " "
        else:
            palavras_chave = ", ".join([p.strip().lower() for p in palavras_chave.split(",")])

        # vincula ao tema
        print("\n--- Vinculação de Tema ---")
        print(f"{Fore.BLUE}AVISO: Se o tema que você precisa não estiver na lista,\nprimeiro cancele ('.') e use a Opção (1) 'Gerenciar Temas' do menu principal.{Style.RESET_ALL}")

        listar_temas() 

        while True:
            id_tema_material = ler_entrada("\nDigite o ID do tema/subtema ao qual este material pertence: ", int)
            if id_tema_material is None: return # Usuário cancelou

            if id_tema_material == 0:
                print(f"\n{erro()} ID inválido. Tente novamente.")
                continue

            # checa se o ID existe na tabela de temas
            cursor.execute("SELECT id FROM temas WHERE id = ?", (id_tema_material,))
            if cursor.fetchone():
                break
            else:
                print(f"\n{erro()} O ID de tema '{id_tema_material}' não existe. Tente novamente.")

        # adiciona no banco
        sql = """
        INSERT INTO materiais (titulo, tipo, nivel, data, link, 
                               palavras_chave, id_tema)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        dados = (titulo, tipo, nivel, data, link, palavras_chave, 
                 id_tema_material)

        try:
            cursor.execute(sql, dados)
            conexao.commit()
            print("\nMaterial registrado com sucesso!")

        except sqlite3.IntegrityError as e: 
            if "UNIQUE constraint failed: materiais.link" in str(e): #
                print(f"\n{erro()} Este link já foi cadastrado anteriormente.")
            else:
                print(f"\n{erro()} Erro de integridade: {e}")

    except Exception as e:
        print(f"\n{erro()} Ocorreu um erro inesperado: {e}")
    
    finally:
        if 'conexao' in locals():
            conexao.close()

# função interna para exibir resultados
def _exibir_resultados(resultados):

    if not resultados:
        print("\nNenhum material encontrado com esse critério.")
        return

    # Trocamos "Tema Principal (1)" por "Tema"
    cabecalhos = ["ID", "Título", "Tipo", "Nível", "Tema"]
    
    print("\n" + tabela_formatada(cabecalhos, resultados) + "\n")


#Função de Consulta
def consultar_materiais():
    
    print("\n=== CONSULTAR MATERIAIS ===")
    
    # query base
    sql_base = """
    FROM materiais m 
    LEFT JOIN temas t ON m.id_tema = t.id
    """
    
    # colunas que queremos mostrar
    sql_colunas = "SELECT m.id, m.titulo, m.tipo, m.nivel, t.nome "

    while True: 
        print(aviso_cancelar()) # Mostra o aviso "Digite . para cancelar"
        
        print("\n(1) Ver todos os materiais cadastrados")
        print("(2) Filtrar por Tipo (artigo, vídeo, etc.)")
        print("(3) Filtrar por Nível (básico, etc.)")
        print("(4) Filtrar por Tema")
        print("(5) Filtrar por Palavra-Chave")
        print("(6) Filtrar por Data Exata (DD/MM/AAAA)")
        print("(0) Voltar ao menu principal")
        
        try:
            acao = ler_entrada("\nEscolha uma opção de consulta: ", int)
            if acao is None: return
            
            if acao == 0:
                print("\nRetornando ao menu principal...")
                break # Sai da função

            sql_final = sql_colunas + sql_base
            params = () 

            if acao == 1:
                print("\n--- Todos os Materiais Cadastrados (Resumo) ---")
                sql_final += "ORDER BY m.id"

            elif acao == 2:
                print("\n--- Filtrar por Tipo ---")
                filtro = ler_entrada("Qual tipo você quer filtrar? (ex: vídeo): ", str)
                if filtro is None: return
                
                sql_final += "WHERE m.tipo = ? ORDER BY m.id"
                params = (filtro.lower(),)

            elif acao == 3:
                print("\n--- Filtrar por Nível ---")
                filtro = ler_entrada("Qual nível você quer filtrar? (ex: básico): ", str)
                if filtro is None: return
                
                sql_final += "WHERE m.nivel = ? ORDER BY m.id"
                params = (filtro.lower(),)

            elif acao == 4:
                print("\n--- Filtrar por Tema ---")
                filtro = ler_entrada("Qual Tema você quer filtrar? (ex: Python): ", str)
                if filtro is None: return
                
                sql_final += "WHERE t.nome LIKE ? ORDER BY m.id"
                params = (f"%{filtro}%",)

            elif acao == 5:
                print("\n--- Filtrar por Palavra-Chave ---")
                filtro = ler_entrada("Qual Palavra-Chave você quer filtrar? (ex: python): ", str)
                if filtro is None: return 
                if not filtro.strip():
                    print(f"\n{erro()} Você não digitou nenhuma palavra-chave.")
                    continue 

                sql_final += "WHERE m.palavras_chave LIKE ? ORDER BY m.id"
                params = (f"%{filtro}%",)

            elif acao == 6:
                print("\n--- Filtrar por Data Exata ---")
                filtro = ler_entrada("Qual Data você quer filtrar? (DD/MM/AAAA): ", str)
                if filtro is None: return
                if not filtro.strip():
                    print(f"\n{erro()} Você não digitou uma data.")
                    continue 
                
                sql_final += "WHERE m.data = ? ORDER BY m.id"
                params = (filtro,)
            
            else:
                print(f"{erro()} Opção inválida.")
                continue 

            # Execução do SQL 
            try:
                conexao = conectar()
                cursor = conexao.cursor()
                
                cursor.execute(sql_final, params)
                resultados = cursor.fetchall()
                _exibir_resultados(resultados) 

            except Exception as e:
                print(f"\n{erro()} Erro ao consultar o banco: {e}")
            finally:
                if 'conexao' in locals():
                    conexao.close()

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número.")


# remove material
def remover_material():

    print("\n=== REMOVER MATERIAL ===")
    print(aviso_cancelar())

    try:
        id_remover = ler_entrada("\nDigite o ID do material que deseja remover: ", int)
        if id_remover is None:
            return

        # confirmação
        while True:
            confirmacao = ler_entrada(f"\nTem certeza que deseja remover o material ID {id_remover}? (S/N): ", str)
            if confirmacao is None: return
            
            if confirmacao.lower() == 's':
                break
            elif confirmacao.lower() == 'n':
                print("\nOperação cancelada.")
                return
            else:
                print(f"\n{erro()} Digite 'S' para sim ou 'N' para não.")

        # remoção 
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "DELETE FROM materiais WHERE id = ?"
        
        cursor.execute(sql, (id_remover,))
        
        if cursor.rowcount > 0:
            conexao.commit()
            print("\nMaterial removido com sucesso!")
        else:
            print(f"\n{erro()} Nenhum material encontrado com o ID {id_remover}.")

    except ValueError:
        print(f"\n{erro()} Entrada inválida. Digite um número de ID.")
    except Exception as e:
        print(f"\n{erro()} Erro ao remover material: {e}")
    finally:
        if 'conexao' in locals():
            conexao.close()

# edita material
def editar_material():
    print("\n=== EDITAR MATERIAL ===")
    print(aviso_cancelar())

    try:
        # pede o ID do material
        id_editar = ler_entrada("\nDigite o ID do material que deseja editar: ", int)
        if id_editar is None: return 

        # busca os dados atuais desse ID (JOIN LEFT -> traz todos os registros de materiais, 
        # mesmo que não tenham correspondência em temas). Se um material não tiver tema associado, 
        # ele ainda aparecerá no resultado, mas os campos da tabela temas virão como NULL
        conexao = conectar()
        cursor = conexao.cursor()
        sql_busca = """
        SELECT m.titulo, m.tipo, m.nivel, m.data, m.link, 
               m.palavras_chave, m.id_tema, t.nome 
        FROM materiais m
        LEFT JOIN temas t ON m.id_tema = t.id
        WHERE m.id = ?
        """
        cursor.execute(sql_busca, (id_editar,))
        dados_atuais = cursor.fetchone()

        if dados_atuais is None:
            print(f"\n{erro()} Nenhum material encontrado com o ID {id_editar}.")
            conexao.close()
            return
        
        # dados atuais
        (titulo, tipo, nivel, data, link, palavras, id_tema_atual, nome_tema_atual) = dados_atuais
        
        print("\n--- Editando Material ---")
        print(f"ID: {id_editar}")
        print("Deixe o campo em branco (só apertar Enter) para manter o valor atual.")

        # pede os novos dados

        novo_titulo = ler_entrada(f"Título [{titulo}]: ", str)
        if novo_titulo is None: return
        if novo_titulo == "": 
            novo_titulo = titulo

        tipos_validos = ['artigo', 'vídeo', 'podcast', 'documentação']
        while True:
            novo_tipo = ler_entrada(f"Tipo [{tipo}]: ", str)
            if novo_tipo is None: return
            if novo_tipo == "":
                novo_tipo = tipo
                break
            if novo_tipo.lower() in tipos_validos:
                tipo = novo_tipo.lower()
                break
            else:
                print(f"\n{erro()} Tipo inválido. Escolha um dos tipos listados.")
        
        niveis_validos = ['básico', 'intermediário', 'avançado']
        while True:
            novo_nivel = ler_entrada(f"Nível [{nivel}]: ", str)
            if novo_nivel is None: return
            if novo_nivel == "":
                novo_nivel = nivel
                break
            if novo_nivel.lower() in niveis_validos:
                nivel = novo_nivel.lower()
                break
            else:
                print(f"\n{erro()} Nível inválido. Escolha um dos níveis listados.")

        novo_data = ler_entrada(f"Data [{data}]: ", str)
        if novo_data is None: return
        if novo_data == "":
            nova_data = data

        novo_link = ler_entrada(f"Link [{link}]: ", str)
        if novo_link is None: return
        if novo_link == "":
            novo_link = link

        novo_palavras = ler_entrada(f"Palavras-chave [{palavras or ''}]: ", str)
        if novo_palavras is None: return
        if novo_palavras == "":
            novo_palavras = palavras

        
        print("\n--- Editando Tema ---")
        # Mostra o tema atual
        if nome_tema_atual:
            print(f"Tema Atual: ({id_tema_atual}) {nome_tema_atual}")
        else:
            print("Tema Atual: (Nenhum)")
        
        # Mostra a árvore de temas para o usuário escolher
        listar_temas()
        
        # Pede o NOVO ID, sugerindo o antigo
        novo_id_tema = ler_entrada(f"Novo ID do Tema [{id_tema_atual}]: ", int)
        if novo_id_tema is None: return
        if novo_id_tema == "":
            novo_id_tema = id_tema_atual

        # atualização do banco de dados

        sql_update = """
        UPDATE materiais SET 
            titulo = ?, tipo = ?, nivel = ?, data = ?, link = ?, 
            palavras_chave = ?, id_tema = ?
        WHERE id = ? 
        """
        
        # tupla com todos os dados novos
        dados_novos = (
            novo_titulo, novo_tipo, nivel, novo_data, novo_link, novo_palavras,
            novo_id_tema,
            id_editar
        )

        cursor.execute(sql_update, dados_novos)
        conexao.commit()
        print("\nMaterial atualizado com sucesso!")

    except ValueError:
        print(f"\n{erro()} Entrada inválida. Digite um número de ID.")
    except Exception as e:
        print(f"\n{erro()} Erro ao editar material: {e}")
    finally:
        if 'conexao' in locals():
            conexao.close() 