from database import criar_banco, conectar
from usuario import login, cadastrarUsuario
from formatacoes import erro
from materiais import registrar_material, consultar_materiais, remover_material, editar_material
from relatorios import gerar_relatorios 
from temas import gerenciar_temas # <--- NOVA IMPORTAÇÃO

# --- Importações do Python ---
from colorama import init

# Inicializa o Colorama (para o 'erro()' funcionar)
init(autoreset=True)

def validarUsuario():
    # (Função validarUsuario() sem mudanças... pode copiar a sua)
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
    print("(2) Consultar materiais") 
    print("(3) Gerar relatórios")
    print("(4) Remover material")
    print("(5) Editar material")
    print("(6) Gerenciar Temas/Subtemas") # <--- NOVA OPÇÃO
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
                    consultar_materiais()
                case 3:
                    gerar_relatorios()
                case 4:
                    remover_material()
                case 5:
                    editar_material()
                case 6:
                    gerenciar_temas() # <--- NOVA CASE
                case 0:
                    print("==================")
                    print("Programa encerrado")
                    print("==================\n")
                    break 
                case _:
                    print(f"{erro()} Entrada inválida. Digite um dos números listados no menu.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número inteiro.")


# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    main()