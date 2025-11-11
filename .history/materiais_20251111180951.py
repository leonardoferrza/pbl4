from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada
import sqlite3 
from datetime import datetime

def registrar_material():
    
    print("\n=== REGISTRAR NOVO MATERIAL ===")
    print(aviso_cancelar())

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # --- Coleta de Dados ---
        
        titulo = ler_entrada("\nTítulo: ", str)
        if titulo is None: return

        # Validação de 'tipo'
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
                print(f"\n{erro()} Entrada inválida. Digite apenas o número da opção.1")

        # Validação de 'nível'
        niveis_validos = ['básico', 'intermediário', 'avançado']
        while True:
            nivel_prompt = f"\nNível ({'/'.join(niveis_validos)}): "
            nivel = ler_entrada(nivel_prompt, str)
            if nivel is None: return
            if nivel.lower() in niveis_validos:
                nivel = nivel.lower()
                break
            else:
                print(f"\n{erro()} Nível inválido. Escolha um dos níveis listados.")

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
        link = ler_entrada("\nLink: ", str)
        if link is None: return
        if not link:
            print(f"\n{erro()} O link é obrigatório.")
            return

        # Opcionais
        palavras_chave = ler_entrada("\nPalavras-chave (separadas por vírgula): ", str)
        if palavras_chave is None: return

        # Hierarquia de Temas
        print("\n--- Organização por Temas (Nível 1 é obrigatório) ---")
        tema_1 = ler_entrada("Tema (Nível 1): ", str)
        if tema_1 is None: return
        if not tema_1:
             print(f"\n{erro()} O Tema de Nível 1 é obrigatório.")
             return

        tema_2 = ler_entrada("Subtema (Nível 2) (opcional): ", str)
        if tema_2 is None: return

        tema_3 = ler_entrada("Subtema (Nível 3) (opcional): ", str)
        if tema_3 is None: return

        tema_4 = ler_entrada("Subtema (Nível 4) (opcional): ", str)
        if tema_4 is None: return

        tema_5 = ler_entrada("Subtema (Nível 5) (opcional): ", str)
        if tema_5 is None: return

        # --- Inserção no Banco ---
        
        sql = """
        INSERT INTO materiais (titulo, tipo, nivel, data, link, palavras_chave,
                               tema_1, tema_2, tema_3, tema_4, tema_5)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        dados = (titulo, tipo, nivel, data, link, palavras_chave, 
                 tema_1, tema_2, tema_3, tema_4, tema_5)

        try:
            cursor.execute(sql, dados)
            conexao.commit()
            print("\nMaterial registrado com sucesso!")

        except sqlite3.IntegrityError:
            print(f"\n{erro()} Este link já foi cadastrado anteriormente.")

    except Exception as e:
        print(f"\n{erro()} Ocorreu um erro inesperado: {e}")
    
    finally:
        if 'conexao' in locals():
            conexao.close()


# --- FUNÇÃO "AJUDANTE" (CORRIGIDA PARA NÃO QUEBRAR A TABELA) ---
def _exibir_resultados(resultados):
    """
    Função interna simples para mostrar os resultados na tabela.
    """
    if not resultados:
        print("\nNenhum material encontrado com esse critério.")
        return

    # Mostramos um resumo (5 colunas) para caber na tela
    cabecalhos = ["ID", "Título", "Tipo", "Nível", "Tema Principal (1)"]
    
    # Usa a função do PBL3 para desenhar a tabela
    print("\n" + tabela_formatada(cabecalhos, resultados))


# --- FUNÇÃO DE CONSULTA (ATUALIZADA COM FILTRO "DATA") ---
def consultar_materiais():
    """
    Mostra um menu para consultar os materiais cadastrados.
    """
    print("\n=== CONSULTAR MATERIAIS ===")
    
    while True: 
        print(aviso_cancelar()) # Mostra o aviso "Digite . para cancelar"
        
        # MUDANÇA AQUI: Adicionamos a nova opção (6)
        print("\n(1) Ver todos os materiais cadastrados")
        print("(2) Filtrar por Tipo (artigo, vídeo, etc.)")
        print("(3) Filtrar por Nível (básico, etc.)")
        print("(4) Filtrar por Tema Principal (Tema 1)")
        print("(5) Filtrar por Palavra-Chave")
        print("(6) Filtrar por Data Exata (DD/MM/AAAA)")
        print("(0) Voltar ao menu principal")
        
        try:
            # Usamos ler_entrada para permitir '.' (cancelar)
            acao = ler_entrada("\nEscolha uma opção de consulta: ", int)
            
            if acao is None or acao == 0:
                print("\nRetornando ao menu principal...")
                break # Sai da função

            # --- Opção (1): Ver Todos ---
            elif acao == 1:
                print("\n--- Todos os Materiais Cadastrados (Resumo) ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais ORDER BY id"
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            # --- Opção (2): Filtrar por Tipo ---
            elif acao == 2:
                print("\n--- Filtrar por Tipo ---")
                
                tipo_filtro = ler_entrada("Qual tipo você quer filtrar? (ex: vídeo): ", str)
                if tipo_filtro is None: 
                    continue 
                
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais WHERE tipo = ? ORDER BY id"
                    
                    cursor.execute(sql, (tipo_filtro.lower(),))
                    resultados = cursor.fetchall()
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()
            
            # --- Opção (3): Filtrar por Nível ---
            elif acao == 3:
                print("\n--- Filtrar por Nível ---")
                
                nivel_filtro = ler_entrada("Qual nível você quer filtrar? (ex: básico): ", str)
                if nivel_filtro is None: 
                    continue 
                
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais WHERE nivel = ? ORDER BY id"
                    
                    cursor.execute(sql, (nivel_filtro.lower(),))
                    resultados = cursor.fetchall()
                    
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            # --- Opção (4): Filtrar por Tema 1 ---
            elif acao == 4:
                print("\n--- Filtrar por Tema Principal ---")
                
                tema_filtro = ler_entrada("Qual Tema Principal você quer filtrar? (ex: artigos): ", str)
                if tema_filtro is None: 
                    continue 
                
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais WHERE tema_1 LIKE ? ORDER BY id"
                    
                    filtro_like = f"%{tema_filtro}%"
                    
                    cursor.execute(sql, (filtro_like,))
                    resultados = cursor.fetchall()
                    
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            # --- Opção (5): Filtrar por Palavra-Chave ---
            elif acao == 5:
                print("\n--- Filtrar por Palavra-Chave ---")
                
                palavra_filtro = ler_entrada("Qual Palavra-Chave você quer filtrar? (ex: python): ", str)
                if palavra_filtro is None: 
                    continue 
                
                if not palavra_filtro.strip():
                    print(f"\n{erro()} Você não digitou nenhuma palavra-chave.")
                    continue 

                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais WHERE palavras_chave LIKE ? ORDER BY id"
                    
                    filtro_like = f"%{palavra_filtro}%"
                    
                    cursor.execute(sql, (filtro_like,))
                    resultados = cursor.fetchall()
                    
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            # --- NOVA OPÇÃO (6): Filtrar por Data ---
            elif acao == 6:
                print("\n--- Filtrar por Data Exata ---")
                
                data_filtro = ler_entrada("Qual Data você quer filtrar? (DD/MM/AAAA): ", str)
                if data_filtro is None: 
                    continue 

                if not data_filtro.strip():
                    print(f"\n{erro()} Você não digitou uma data.")
                    continue 
                
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    # SQL (busca exata) para filtrar pela coluna 'data'
                    sql = "SELECT id, titulo, tipo, nivel, tema_1 FROM materiais WHERE data = ? ORDER BY id"
                    
                    cursor.execute(sql, (data_filtro,))
                    resultados = cursor.fetchall()
                    
                    _exibir_resultados(resultados) 

                except Exception as e:
                    print(f"\n{erro()} Erro ao consultar o banco: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            else:
                print(f"\n{erro()} Opção inválida.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número.")

# --- FUNÇÃO PARA REMOVER MATERIAL (EXISTENTE) ---
def remover_material():
    """
    Remove um material do banco de dados com base no ID.
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


# --- FUNÇÃO PARA EDITAR MATERIAL (EXISTENTE) ---
def editar_material():
    """
    Edita um material existente no banco de dados com base no ID.
    """
    print("\n=== EDITAR MATERIAL ===")
    print(aviso_cancelar())

    try:
        # 1. Pede o ID do material
        id_editar = ler_entrada("\nDigite o ID do material que deseja editar: ", int)
        if id_editar is None:
            return # Usuário cancelou

        # 2. Busca os dados atuais desse ID
        conexao = conectar()
        cursor = conexao.cursor()
        sql_busca = "SELECT titulo, tipo, nivel, data, link, palavras_chave, tema_1, tema_2, tema_3, tema_4, tema_5 FROM materiais WHERE id = ?"
        cursor.execute(sql_busca, (id_editar,))
        dados_atuais = cursor.fetchone()

        if dados_atuais is None:
            print(f"\n{erro()} Nenhum material encontrado com o ID {id_editar}.")
            conexao.close()
            return
        
        # Separa os dados atuais
        (titulo, tipo, nivel, data, link, palavras, t1, t2, t3, t4, t5) = dados_atuais
        
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
        
        print("\n--- Editando Temas ---")
        novo_t1 = ler_entrada(f"Tema 1 [{t1}]: ", str) or t1
        novo_t2 = ler_entrada(f"Tema 2 [{t2 or ''}]: ", str) or t2
        novo_t3 = ler_entrada(f"Tema 3 [{t3 or ''}]: ", str) or t3
        novo_t4 = ler_entrada(f"Tema 4 [{t4 or ''}]: ", str) or t4
        novo_t5 = ler_entrada(f"Tema 5 [{t5 or ''}]: ", str) or t5

        # 4. Execução da Atualização (SQL UPDATE)
        
        sql_update = """
        UPDATE materiais SET 
            titulo = ?, tipo = ?, nivel = ?, data = ?, link = ?, 
            palavras_chave = ?, tema_1 = ?, tema_2 = ?, tema_3 = ?, 
            tema_4 = ?, tema_5 = ?
        WHERE id = ? 
        """
        
        dados_novos = (
            novo_titulo, tipo, nivel, novo_data, novo_link, novo_palavras,
            novo_t1, novo_t2, novo_t3, novo_t4, novo_t5,
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