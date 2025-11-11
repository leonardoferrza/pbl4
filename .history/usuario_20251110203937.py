from database import conectar
from formatacoes import erro

def cadastrarUsuario():
    print("\n=== CADASTRO ===\n")
    username = input("Username: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO usuario (username, senha) VALUES (?, ?)", (username, senha))
        conexao.commit()
        print("\nUsuário cadastrado com sucesso!")
    except Exception as e:
        print(f"\n{erro()} Erro ao cadastrar usuário: {e}")
    finally:
        conexao.close()


def login():
    limiteDeErros = 3
    conexao = conectar()
    cursor = conexao.cursor()

    print("\n=== LOGIN ===\n")

    while limiteDeErros > 0:
        username = input("Username: ")
        senha = input("Senha: ")

        cursor.execute("SELECT id FROM usuario WHERE username = ? AND senha = ?", (username, senha))
        if cursor.fetchone():
            print("\nUsuário logado com sucesso!")
            conexao.close()
            return 1
        else:
            limiteDeErros -= 1
            print(f"\n{erro()} Usuário ou senha incorreto. Tente novamente.\n")
    
    print("\nLimite de erros atingido.")
    conexao.close()
    return 0