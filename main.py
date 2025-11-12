from database import criar_banco, conectar
from usuario import login, cadastrarUsuario
from formatacoes import erro
from materiais import registrar_material, consultar_materiais, remover_material, editar_material
from relatorios import gerar_relatorios 
from temas import gerenciar_temas


from colorama import init

init(autoreset=True)

def validarUsuario():
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuario")
    existeCadastro = cursor.fetchone()[0]
    conexao.close()

    if existeCadastro:
        print("\nFaça seu login para continuar")
        if login():
            return 1 
        else:
            return validarUsuario()
    else:
        print("\nCadastre-se para começar")
        cadastrarUsuario()
        return 1

def menu_principal():
    print("\n===========================================")
    print(" 📚 GERENCIADOR DE MATERIAIS DE ESTUDO 📚")
    print("===========================================")
    print("(1) Gerenciar Temas/Subtemas") 
    print("(2) Registrar novo material") 
    print("(3) Consultar materiais") 
    print("(4) Gerar relatórios") 
    print("(5) Remover material") 
    print("(6) Editar material") 
    print("(0) Sair")
    print("--------------------------------------")


def main():
    print("\n=============")
    print("BEM-VINDO(A)!")
    print("=============")

    criar_banco()

    if not validarUsuario():
        print("\nFalha na autenticação. Encerrando.")
        return

    while True:
        menu_principal()
        
        try:
            acao = int(input("\nEscolha uma opção: "))
            print()

            match acao:
                case 1:
                    gerenciar_temas() 
                case 2:
                    registrar_material() 
                case 3:
                    consultar_materiais() 
                case 4:
                    gerar_relatorios() 
                case 5:
                    remover_material() 
                case 6:
                    editar_material() 
                case 0:
                    print("==================")
                    print("Programa encerrado")
                    print("==================\n")
                    break 
                case _:
                    print(f"{erro()} Entrada inválida. Digite um dos números listados no menu.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número inteiro.")
 
if __name__ == "__main__":
    main()