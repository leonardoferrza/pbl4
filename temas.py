from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro

# --- Funções de Listagem (A parte mais importante) ---

def _mostrar_temas_recursivo(cursor, id_pai, nivel):
    """
    Função "mágica" interna que busca os subtemas
    e se chama novamente, aumentando o recuo (nível).
    """
    # Encontra todos os temas que são "filhos" do id_pai atual
    if id_pai is None:
        sql = "SELECT id, nome FROM temas WHERE id_pai IS NULL ORDER BY nome"
        cursor.execute(sql)
    else:
        sql = "SELECT id, nome FROM temas WHERE id_pai = ? ORDER BY nome"
        cursor.execute(sql, (id_pai,))
    
    resultados = cursor.fetchall()
    
    # Imprime cada tema filho com o recuo
    for (id_tema, nome) in resultados:
        recuo = "  " * nivel # Cria o recuo (ex: Nível 2 = "    ")
        print(f"{recuo}- ({id_tema}) {nome}")
        
        # MÁGICA (Recursão):
        # Pede para esta mesma função encontrar os filhos DESTE tema
        _mostrar_temas_recursivo(cursor, id_tema, nivel + 1)

def listar_temas():
    """
    Mostra a árvore de temas e subtemas completa.
    """
    print("\n--- Árvore de Temas Atuais ---")
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        # Começa a busca "mágica" a partir do topo (id_pai = None)
        _mostrar_temas_recursivo(cursor, None, 0)
        
    except Exception as e:
        print(f"\n{erro()} Erro ao listar temas: {e}")
    finally:
        if 'conexao' in locals():
            conexao.close()
    print("-" * 30)


# --- Funções de Gerenciamento ---

def criar_tema():
    """
    Adiciona um novo tema ou subtema no banco.
    """
    print("\n=== CRIAR NOVO TEMA/SUBTEMA ===")
    
    # Mostra a árvore atual para o usuário saber onde quer adicionar
    listar_temas()
    print("Você pode criar um tema principal (Nível 1) ou um subtema.")
    print(aviso_cancelar())
    
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        nome = ler_entrada("\nNome do novo tema: ", str)
        if nome is None: return

        # Pergunta qual é o "Pai" deste tema
        id_pai = ler_entrada("Digite o ID do Tema 'Pai' (ou 0 para Tema Principal): ", int)
        if id_pai is None: return

        if id_pai == 0:
            id_pai = None # Nível 1 (sem pai)
        
        # Insere no banco
        sql = "INSERT INTO temas (nome, id_pai) VALUES (?, ?)"
        cursor.execute(sql, (nome, id_pai))
        conexao.commit()
        
        print(f"\nTema '{nome}' criado com sucesso!")

    except Exception as e:
        print(f"\n{erro()} Erro ao criar tema: {e}")
    finally:
        if 'conexao' in locals():
            conexao.close()

def remover_tema():
    """
    Remove um tema, mas só se ele não tiver subtemas ou materiais.
    """
    print("\n=== REMOVER TEMA/SUBTEMA ===")
    listar_temas()
    print(f"\n{erro()} ATENÇÃO: Você só pode remover um tema se ele estiver VAZIO\n(sem subtemas e sem materiais vinculados a ele).")
    print(aviso_cancelar())

    try:
        id_remover = ler_entrada("\nDigite o ID do tema que deseja remover: ", int)
        if id_remover is None: return

        conexao = conectar()
        cursor = conexao.cursor()

        # 1. Verifica se o tema tem subtemas (filhos)
        sql_check_filhos = "SELECT COUNT(*) FROM temas WHERE id_pai = ?"
        cursor.execute(sql_check_filhos, (id_remover,))
        contagem_filhos = cursor.fetchone()[0]
        
        if contagem_filhos > 0:
            print(f"\n{erro()} Não é possível remover. O Tema ID {id_remover} possui {contagem_filhos} subtemas.")
            return

        # 2. Verifica se o tema tem materiais ligados a ele
        sql_check_materiais = "SELECT COUNT(*) FROM materiais WHERE id_tema = ?"
        cursor.execute(sql_check_materiais, (id_remover,))
        contagem_materiais = cursor.fetchone()[0]

        if contagem_materiais > 0:
            print(f"\n{erro()} Não é possível remover. O Tema ID {id_remover} está sendo usado por {contagem_materiais} materiais.")
            return

        # 3. Se passou nas duas checagens, pode remover
        sql_delete = "DELETE FROM temas WHERE id = ?"
        cursor.execute(sql_delete, (id_remover,))
        
        if cursor.rowcount > 0:
            conexao.commit()
            print("\nTema removido com sucesso!")
        else:
            print(f"\n{erro()} Nenhum tema encontrado com o ID {id_remover}.")

    except Exception as e:
        print(f"\n{erro()} Erro ao remover tema: {e}")
    finally:
        if 'conexao' in locals():
            conexao.close()


# --- Função Principal do Módulo ---

def gerenciar_temas():
    """
    Mostra o sub-menu de gerenciamento de temas.
    """
    while True:
        print("\n--- GERENCIAMENTO DE TEMAS ---")
        print("(1) Listar todos os temas (Árvore)")
        print("(2) Criar novo tema/subtema")
        print("(3) Remover tema/subtema")
        print("(0) Voltar ao menu principal")
        
        try:
            acao = ler_entrada("\nEscolha uma opção: ", int)
            if acao is None or acao == 0:
                print("\nRetornando ao menu principal...")
                break
            
            match acao:
                case 1:
                    listar_temas()
                case 2:
                    criar_tema()
                case 3:
                    remover_tema()
                case _:
                    print(f"{erro()} Opção inválida.")
        
        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número.")