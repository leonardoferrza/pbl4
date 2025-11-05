from colorama import Fore, Style, init
from tabulate import tabulate

def erro():
    return Style.BRIGHT + Fore.RED + "ERRO:" + Style.RESET_ALL

def tabela_formatada(cabecalhos, resultados):
    alinhamento =  ["left"] * len(cabecalhos)
    return tabulate(resultados, headers=cabecalhos, tablefmt="simple", colalign=alinhamento)

def ler_entrada(mensagem, tipo=str):
    while True:
        entrada = input(mensagem)
        if entrada.strip() == ".":
            print(Style.BRIGHT + Fore.RED + "\nOperação cancelada. " + Style.RESET_ALL + "Retornando ao menu principal...")
            return None
        try:
            return tipo(entrada)
        except ValueError:
            print(f"\n{erro()} Entrada inválida. Tente novamente ou digite '.' para cancelar.")
    
def aviso_cancelar():
    return Fore.BLUE + "Insira '.' para cancelar a operação e retornar ao menu."