# Arquivo: PBL4/materiais.py

from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada
import sqlite3 
from datetime import datetime

#
# SUA FUNÇÃO DE REGISTRO (EXISTENTE)
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

        # Validação de 'tipo'
        tipos_validos = ['artigo', 'vídeo', 'podcast', 'documentação']
        while True:
            tipo_prompt = f"\nTipo ({'/'.join(tipos_validos)}): "
            tipo = ler_entrada(tipo_prompt, str)
            if tipo is None: return
            if tipo.lower() in tipos_validos:
                tipo = tipo.lower()
                break
            else:
                print(f"\n{erro()} Tipo inválido. Escolha um dos tipos listados.")

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
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        data_prompt = f"\nData (DD/MM/AAAA ou Enter para hoje - {data_hoje}): "
        data = ler_entrada(data_prompt, str)
        if data is None: return
        if data == "":
            data = data_hoje

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


# --- NOVA FUNÇÃO "AJUDANTE" PARA MOSTRAR A TABELA ---
def _exibir_resultados(resultados):
    """
    Função interna simples para mostrar os resultados na tabela.
    """
    if not resultados:
        print("\nNenhum material encontrado com esse critério.")
        return

    # Define os títulos da nossa tabela
    cabecalhos = ["ID", "Título", "Tipo", "Nível", "Data", "Link", 
                  "Palavras-Chave", "Tema 1", "Tema 2", "Tema 3", "Tema 4", "Tema 5"]
    
    # [cite_start]Usa a função do PBL3 para desenhar a tabela [cite: 55-57]
    print("\n" + tabela_formatada(cabecalhos, resultados))


# --- NOVA FUNÇÃO PRINCIPAL DE CONSULTA ---
def consultar_materiais():
    """
    Mostra um menu para consultar os materiais cadastrados.
    """
    print("\n=== CONSULTAR MATERIAIS ===")
    
    while True: 
        print(aviso_cancelar()) # Mostra o aviso "Digite . para cancelar"
        print("\n(1) Ver todos os materiais cadastrados")
        print("(0) Voltar ao menu principal")
        
        try:
            # [cite_start]Usamos ler_entrada [cite: 58-61] para permitir '.' (cancelar)
            acao = ler_entrada("\nEscolha uma opção de consulta: ", int)
            
            if acao is None or acao == 0:
                print("\nRetornando ao menu principal...")
                break # Sai da função

            elif acao == 1:
                print("\n--- Todos os Materiais Cadastrados ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    cursor.execute("SELECT * FROM materiais ORDER BY id")
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