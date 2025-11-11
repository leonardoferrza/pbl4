from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada

def gerar_relatorios():
    """
    Mostra um menu para gerar relatórios e estatísticas.
    """
    print("\n=== GERAR RELATÓRIOS ===")
    
    while True:
        print(aviso_cancelar()) # Mostra "Insira '.' para cancelar"
        
        # MUDANÇA AQUI: Adicionamos a nova opção (3)
        print("\n(1) Contagem de materiais por Tipo")
        print("(2) Contagem de materiais por Nível")
        print("(3) Contagem de materiais por Tema Principal (Tema 1)")
        print("(0) Voltar ao menu principal")
        
        try:
            acao = ler_entrada("\nEscolha uma opção de relatório: ", int)
            
            if acao is None or acao == 0:
                print("\nRetornando ao menu principal...")
                break # Sai do loop 'while True'

            # --- Opção (1): Contagem por Tipo ---
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
            
            # --- Opção (2): Contagem por Nível ---
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

            # --- NOVA OPÇÃO (3): Contagem por Tema 1 ---
            elif acao == 3:
                print("\n--- Relatório: Contagem por Tema Principal ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    # SQL de Agregação (só muda o 'GROUP BY')
                    sql = "SELECT tema_1, COUNT(*) FROM materiais GROUP BY tema_1"
                    
                    cursor.execute(sql)
                    resultados = cursor.fetchall()
                    
                    # Novos cabeçalhos
                    cabecalhos = ["Tema Principal (Tema 1)", "Quantidade Registrada"]
                    
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