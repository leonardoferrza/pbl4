# Arquivo: PBL4/main.py

# --- Importações de outros arquivos do PBL4 ---
from database import criar_banco, conectar
from usuario import login, cadastrarUsuario
from formatacoes import erro
from materiais import registrar_material, consultar_materiais # < IMPORTAÇÃO CORRIGIDA

# --- Importações do Python ---
from colorama import init

# Inicializa o Colorama (para o 'erro()' funcionar)
init(autoreset=True)

def validarUsuario():
    """
    Verifica se existe um usuário cadastrado.
    (Lógica adaptada do PBL3)
    """
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuario")
    existeCadastro = cursor.fetchone()[0]
    conexao.close()

    if existeCadastro:
        print("\nFaça seu login para continuar")
        if login():
            return 1 # Login com sucesso
        else:
            return validarUsuario() # Tenta de novo
    else:
        print("\nCadastre-se para começar")
        cadastrarUsuario()
        return 1 # Cadastro com sucesso


def menu_principal():
    """Mostra o menu de opções do PBL4."""
    print("\n======================================")
    print(" $ GERENCIADOR DE MATERIAIS DE ESTUDO $")
    print("======================================")
    print("(1) Registrar novo material")
    print("(2) Consultar materiais") # < TEXTO CORRIGIDO
    print("(3) Relatórios (em breve)")
    print("(0) Sair")
    print("--------------------------------------")


# --- Função Principal do Programa ---
def main():
    print("\n=============")
    print("BEM-VINDO(A)!")
    print("=============")

    # 1. Garante que o banco e as tabelas existam
    criar_banco()

    # 2. Valida o usuário (força login ou cadastro)
    if not validarUsuario():
        print("\nFalha na autenticação. Encerrando.")
        return # Encerra o programa se a validação falhar

    # 3. Loop do Menu Principal
    while True:
        menu_principal()
        
        try:
            acao = int(input("\nEscolha uma opção: "))
            print() # Adiciona uma linha em branco

            match acao:
                case 1:
                    registrar_material()
                case 2:
                    consultar_materiais() # < CASE 2 CORRIGIDA
                case 3:
                    print("Função de relatórios ainda não implementada.")
                case 0:
                    print("==================")
                    print("Programa encerrado")
                    print("==================\n")
                    break # Quebra o loop 'while True' e encerra
                case _:
                    print(f"{erro()} Entrada inválida. Digite um dos números listados no menu.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número inteiro.")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    main()