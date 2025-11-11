# Arquivo: PBL4/relatorios.py (VERSÃO FINAL REFATORADA)

from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada

def gerar_relatorios():
    """
    Mostra um menu para gerar relatórios (NOVO SISTEMA DE TEMAS).
    """
    print("\n=== GERAR RELATÓRIOS ===")
    
    while True:
        print(aviso_cancelar()) # Mostra "Insira '.' para cancelar"
        
        # MUDANÇA AQUI: Ajustámos o nome da opção 3
        print("\n(1) Contagem de materiais por Tipo")
        print("(2) Contagem de materiais por Nível")
        print("(3) Contagem de materiais por Tema")
        print("(4) Contagem de materiais por Mês/Ano")
        print("(0) Voltar ao menu principal")
        
        try:
            acao = ler_entrada("\nEscolha uma opção de relatório: ", int)
            
            if acao is None or acao == 0:
                print("\nRetornando ao menu principal...")
                break # Sai do loop 'while True'

            # --- Opção (1): Contagem por Tipo (Sem mudança) ---
            elif acao == 1:
                print("\n--- Relatório: Contagem por Tipo ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT tipo, COUNT(*) FROM materiais GROUP BY tipo"
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    
                    cabecalhos = ["Tipo de Material", "Quantidade Registrada"]
                    print("\n" + tabela_formatada(cabecalhos, resultados))

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()
            
            # --- Opção (2): Contagem por Nível (Sem mudança) ---
            elif acao == 2:
                print("\n--- Relatório: Contagem por Nível ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = "SELECT nivel, COUNT(*) FROM materiais GROUP BY nivel"
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    
                    cabecalhos = ["Nível do Material", "Quantidade Registrada"]
                    print("\n" + tabela_formatada(cabecalhos, resultados))

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            # --- OPÇÃO (3): Contagem por Tema (REFATORADA) ---
            elif acao == 3:
                print("\n--- Relatório: Contagem por Tema ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    # MUDANÇA AQUI: Usamos JOIN para buscar o nome do tema
                    sql = """
                    SELECT 
                        t.nome, 
                        COUNT(m.id) 
                    FROM materiais m
                    LEFT JOIN temas t ON m.id_tema = t.id
                    GROUP BY t.nome
                    """
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    
                    # Novos cabeçalhos
                    cabecalhos = ["Tema", "Quantidade Registrada"]
                    
                    print("\n" + tabela_formatada(cabecalhos, resultados))

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()
            
            # --- Opção (4): Contagem por Mês/Ano (Sem mudança) ---
            elif acao == 4:
                print("\n--- Relatório: Contagem por Mês/Ano ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = """
                    SELECT 
                        SUBSTR(data, 4, 7) as MesAno, 
                        COUNT(*) 
                    FROM materiais 
                    GROUP BY MesAno
                    ORDER BY SUBSTR(data, 7, 4), SUBSTR(data, 4, 2)
                    """
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    
                    cabecalhos = ["Mês/Ano", "Quantidade Registrada"]
                    
                    print("\n" + tabela_formatada(cabecalhos, resultados))

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            else:
                print(f"\n{erro()} Opção inválida.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número.")