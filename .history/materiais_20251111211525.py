# Arquivo: PBL4/materiais.py (COM AVISO E SUAS MELHORIAS)

from database import conectar
from temas import listar_temas
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada
import sqlite3 
from datetime import datetime
from colorama import Fore, Style # <--- MODIFICAÇÃO 1 (Importação)

#
# FUNÇÃO DE REGISTRO (COM SUAS MELHORIAS)
#
def registrar_material():
    """
    Registra um novo material de estudo no banco de dados.
    """
    print("\n=== REGISTRAR NOVO MATERIAL ===")
    print(aviso_cancelar())

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # --- Coleta de Dados ---
        
        titulo = ler_entrada("\nTítulo: ", str)
        if titulo is None: return

        # Validação de 'tipo' (Seu código melhorado)
        tipos_validos = ['artigo', 'vídeo', 'podcast', 'documentação']
        
        while True:
            print("\nEscolha o tipo de material:")
            for n, tipos in enumerate(tipos_validos, start=1):
                print(f"{n}. {tipos.capitalize()}")
            
            try:
                escolha_tipo = int(input("\nDigite o número correspondente: "))
                if 1 <= escolha_tipo <= len(tipos_validos):
                    tipo = tipos_validos[escolha_tipo - 1]
                    break
                else:
                    print(f"\n{erro()} Entrada inválida. Escolha um entre 1 e {len(tipos_validos)}.")
            except ValueError:
                print(f"\n{erro()} Entrada inválida. Digite apenas o número da opção.")

        # Validação de 'nível' (Seu código melhorado)
        niveis_validos = ['básico', 'intermediário', 'avançado']
        
        while True:
            print("\nEscolha o nível:")
            for n, niveis in enumerate(niveis_validos, start=1):
                print(f"{n}. {niveis.capitalize()}")

            try:
                escolha_nivel = ler_entrada("\nDigite o número correspondente:", int)
                if escolha_nivel is None:
                    return
                nivel = niveis_validos[escolha_nivel - 1]
                break
            except (ValueError, IndexError):
                print(f"\n{erro()} Entrada inválida. Escolha um entre 1 e {len(niveis_validos)}.")
            
        # Data (com valor padrão) (Seu código melhorado)
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


        # Link (obrigatório) (Seu código melhorado)
        while True:
            link = ler_entrada("\nLink (URL): ", str)
            if link is None:
                return
            if not link.strip():
                
            print(f"\n{erro()} O link é obrigatório.")
                continue

            # Verificação no banco
            cursor.execute("SELECT id FROM materiais WHERE link = ?", (link,))
            if cursor.fetchone():
                print(f"\n{erro()} Este link já foi cadastrado. Tente outro.")
                continue
            else:
                break

        # Opcionais (Seu código melhorado)
        palavras_chave = ler_entrada("\nPalavras-chave (separadas por vírgula): ", str)
        if palavras_chave is None:
            return
        
        palavras_chave = palavras_chave.strip()

        if not palavras_chave:
            palavras_chave = " " # Mantive o seu " "
        else:
            palavras_chave = ", ".join([p.strip().lower() for p in palavras_chave.split(",")])

        # --- Vinculação de Tema (Novo Sistema) ---
        print("\n--- Vinculação de Tema ---")

        # --- MODIFICAÇÃO 2 (Aviso) ---
        print(f"{Fore.BLUE}AVISO: Se o tema que você precisa não estiver na lista,\nprimeiro cancele ('.') e use a Opção (1) 'Gerenciar Temas' do menu principal.{Style.RESET_ALL}")
        
        listar_temas()
        
        id_tema_material = ler_entrada("\nDigite o ID do tema/subtema ao qual este material pertence: ", int)
        if id_tema_material is None: return
        if id_tema_material == 0:
            print(f"\n{erro()} ID inválido.")
            return

        # --- Inserção no Banco (Novo Sistema) ---
        
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
            if "UNIQUE constraint failed: materiais.link" in str(e):
                print(f"\n{erro()} Este link já foi cadastrado anteriormente.")
            elif "FOREIGN KEY constraint failed" in str(e):
                 print(f"\n{erro()} O ID de tema '{id_tema_material}' não existe.")
            else:
                print(f"\n{erro()} Erro de integridade: {e}")

    except Exception as e:
        print(f"\n{erro()} Ocorreu um erro inesperado: {e}")
    
    finally:
        if 'conexao' in locals():
            conexao.close()

#
# (O resto do seu arquivo, com as funções 'consultar', 'remover' e 'editar', continua aqui...)
#

# --- FUNÇÃO "AJUDANTE" (REFATORADA) ---
def _exibir_resultados(resultados):
    """
    Função interna simples para mostrar os resultados (agora com o nome do TEMA).
    """
    if not resultados:
        print("\nNenhum material encontrado com esse critério.")
        return

    # Trocamos "Tema Principal (1)" por "Tema"
    cabecalhos = ["ID", "Título", "Tipo", "Nível", "Tema"]
    
    print("\n" + tabela_formatada(cabecalhos, resultados))


# --- FUNÇÃO DE CONSULTA (REFATORADA COM JOIN) ---
def consultar_materiais():
    """
    Mostra um menu para consultar os materiais (NOVO SISTEMA DE TEMAS).
    """
    print("\n=== CONSULTAR MATERIAIS ===")
    
    # SQL Base (A parte que se repete)
    sql_base = """
    FROM materiais m 
    LEFT JOIN temas t ON m.id_tema = t.id
    """
    
    # Colunas que queremos mostrar (o resumo)
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
            
            if acao is None or acao == 0:
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
                if filtro is None: continue 
                
                sql_final += "WHERE m.tipo = ? ORDER BY m.id"
                params = (filtro.lower(),)

            elif acao == 3:
                print("\n--- Filtrar por Nível ---")
                filtro = ler_entrada("Qual nível você quer filtrar? (ex: básico): ", str)
                if filtro is None: continue 
                
                sql_final += "WHERE m.nivel = ? ORDER BY m.id"
                params = (filtro.lower(),)

            elif acao == 4:
                print("\n--- Filtrar por Tema ---")
                filtro = ler_entrada("Qual Tema você quer filtrar? (ex: Python): ", str)
                if filtro is None: continue 
                
                sql_final += "WHERE t.nome LIKE ? ORDER BY m.id"
                params = (f"%{filtro}%",)

            elif acao == 5:
                print("\n--- Filtrar por Palavra-Chave ---")
                filtro = ler_entrada("Qual Palavra-Chave você quer filtrar? (ex: python): ", str)
                if filtro is None: continue 
                if not filtro.strip():
                    print(f"\n{erro()} Você não digitou nenhuma palavra-chave.")
                    continue 

                sql_final += "WHERE m.palavras_chave LIKE ? ORDER BY m.id"
                params = (f"%{filtro}%",)

            elif acao == 6:
                print("\n--- Filtrar por Data Exata ---")
                filtro = ler_entrada("Qual Data você quer filtrar? (DD/MM/AAAA): ", str)
                if filtro is None: continue 
                if not filtro.strip():
                    print(f"\n{erro()} Você não digitou uma data.")
                    continue 
                
                sql_final += "WHERE m.data = ? ORDER BY m.id"
                params = (filtro,)
            
            else:
                print(f"{erro()} Opção inválida.")
                continue 

            # --- Execução do SQL (Comum a todos) ---
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


# --- FUNÇÃO PARA REMOVER MATERIAL (JÁ REFATORADA) ---
def remover_material():
    """
    Remove um material do banco de dados com base no ID. (REFATORADO)
    """
    print("\n=== REMOVER MATERIAL ===")
    print(aviso_cancelar())

    try:
        id_remover = ler_entrada("\nDigite o ID do material que deseja remover: ", int)
        if id_remover is None:
            return # Usuário cancelou

        # --- Confirmação ---
        while True:
            confirmacao = ler_entrada(f"\nTem certeza que deseja remover o material ID {id_remover}? (S/N): ", str)
            if confirmacao is None:
                return # Usuário cancelou
            
            if confirmacao.lower() == 's':
                break # Sim, quer remover
            elif confirmacao.lower() == 'n':
                print("\nOperação cancelada.")
                return # Não, volta ao menu
            else:
                print(f"\n{erro()} Digite 'S' para sim ou 'N' para não.")

        # --- Execução da Remoção ---
        conexao = conectar()
        cursor = conexao.cursor()
        
        sql = "DELETE FROM materiais WHERE id = ?"
        
        cursor.execute(sql, (id_remover,))
        
        if cursor.rowcount > 0:
            conexao.commit() # Salva a remoção permanentemente
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


# --- FUNÇÃO PARA EDITAR MATERIAL (JÁ REFATORADA) ---
def editar_material():
    """
    Edita um material existente (NOVO SISTEMA DE TEMAS).
    """
    print("\n=== EDITAR MATERIAL ===")
    print(aviso_cancelar())

    try:
        # 1. Pede o ID do material
        id_editar = ler_entrada("\nDigite o ID do material que deseja editar: ", int)
        if id_editar is None: return 

        # 2. Busca os dados atuais desse ID (usando JOIN)
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
        
        # Separa os dados atuais
        (titulo, tipo, nivel, data, link, palavras, id_tema_atual, nome_tema_atual) = dados_atuais
        
        print("\n--- Editando Material ---")
        print(f"ID: {id_editar}")
        print("Deixe o campo em branco (só apertar Enter) para manter o valor atual.")

        # 3. Pede os novos dados (um por um)
        novo_titulo = ler_entrada(f"Título [{titulo}]: ", str) or titulo

        # Validação de 'tipo'
        tipos_validos = ['artigo', 'vídeo', 'podcast', 'documentação']
        while True:
            novo_tipo = ler_entrada(f"Tipo [{tipo}]: ", str) or tipo
            if novo_tipo.lower() in tipos_validos:
                tipo = novo_tipo.lower()
                break
            else:
                print(f"\n{erro()} Tipo inválido. Escolha um dos tipos listados.")
        
        # Validação de 'nível'
        niveis_validos = ['básico', 'intermediário', 'avançado']
        while True:
            novo_nivel = ler_entrada(f"Nível [{nivel}]: ", str) or nivel
            if novo_nivel.lower() in niveis_validos:
                nivel = novo_nivel.lower()
                break
            else:
                print(f"\n{erro()} Nível inválido. Escolha um dos níveis listados.")

        novo_data = ler_entrada(f"Data [{data}]: ", str) or data
        novo_link = ler_entrada(f"Link [{link}]: ", str) or link
        novo_palavras = ler_entrada(f"Palavras-chave [{palavras or ''}]: ", str) or palavras
        
        print("\n--- Editando Tema ---")
        # Mostra o tema atual
        if nome_tema_atual:
            print(f"Tema Atual: ({id_tema_atual}) {nome_tema_atual}")
        else:
            print("Tema Atual: (Nenhum)")
        
        # Mostra a árvore de temas para o usuário escolher
        listar_temas()
        
        # Pede o NOVO ID, sugerindo o antigo
        novo_id_tema = ler_entrada(f"Novo ID do Tema [{id_tema_atual}]: ", int) or id_tema_atual

        # 4. Execução da Atualização (SQL UPDATE)
        
        sql_update = """
        UPDATE materiais SET 
            titulo = ?, tipo = ?, nivel = ?, data = ?, link = ?, 
            palavras_chave = ?, id_tema = ?
        WHERE id = ? 
        """
        
        # Tupla com todos os dados novos (SQL agora é mais curto)
        dados_novos = (
            novo_titulo, tipo, nivel, novo_data, novo_link, novo_palavras,
            novo_id_tema,
            id_editar # O ID é o último, para o 'WHERE id = ?'
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