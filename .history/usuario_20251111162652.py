from database import conectar
from formatacoes import erro

def cadastrarUsuario():
    print("\n=== CADASTRO ===\n")
    username = input("Username: ")
    senha = input("Senha: ")

    conexao = conectar()
    cursor = conexao.cursor()

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
            return 1
        else:
            limiteDeErros -= 1
            print(f"\n{erro()} Usuário ou senha incorreto. Tente novamente.\n")
    
    print("\nLimite de erros atingido.")
    return 0