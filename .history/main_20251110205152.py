from database import *
from usuario import *
from materiais import *
from colorama import Fore, init
from formatacoes import *

init(autoreset=True)


print("\n=============")
print("BEM-VINDO(A)!")
print("=============")

criar_banco()

# --- Validação de Usuário ---
def validarUsuario():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuario")
    existeCadastro = cursor.fetchone()[0]
    conexao.close()

    # Se existe usuário, pede login
    if existeCadastro:
        print("\nFaça seu login para continuar")
        if login():
            return True
        else:
            # recursão leve: tenta novamente o login
            return validarUsuario()
    else:
        print("\nCadastre-se para começar")
        cadastrarUsuario()
        return True


# --- Menu principal ---
def menu():
    print("\n==============================")
    print(" SISTEMA DE GERENCIAMENTO DE ESTUDOS ")
    print("==============================")
    print("(1) Registrar material")
    print("(2) Listar materiais")
    print("(3) Consultar materiais (filtros)")
    print("(4) Gerar relatórios")
    print("(0) Sair")
    print("------------------------------")


# --- Execução principal ---
if validarUsuario():
    while True:
        menu()
        try:
            acao = int(input("\nEscolha uma opção: "))
            print()
            match acao:
                case 1:
                    registrar_materiais()
                case 2:
                    # depois vocês implementam listar_materiais()
                    print("\nFunção ainda não implementada.")
                case 3:
                    # depois vocês implementam consultas personalizadas
                    print("\nFunção ainda não implementada.")
                case 4:
                    # depois vocês implementam relatórios
                    print("\nFunção ainda não implementada.")
                case 0:
                    print("==================")
                    print("Programa encerrado")
                    print("==================\n")
                    break
                case _:
                    print(f"{erro()} Entrada inválida. Digite um dos números listados no menu.")
        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número inteiro.")