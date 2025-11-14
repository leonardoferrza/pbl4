from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro, tabela_formatada

def gerar_relatorios():

    print("\n=== GERAR RELATÓRIOS ===")
    
    while True:
        print(aviso_cancelar())
        
        print("\n(1) Contagem de materiais por Tipo")
        print("(2) Contagem de materiais por Nível")
        print("(3) Contagem de materiais por Tema")
        print("(4) Contagem de materiais por Mês/Ano")
        print("(5) Média de materiais registrados por Mês")
        print("(0) Voltar ao menu principal")
        
        try:
            acao = ler_entrada("\nEscolha uma opção de relatório: ", int)
            
            if acao is None: return
            if acao == 0:
                print("\nRetornando ao menu principal...")
                break

            # contagem por tipo
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
            
            # contagem por nivel
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

            # contagem por tema
            elif acao == 3:
                print("\n--- Relatório: Contagem por Tema ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
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
                    
                    cabecalhos = ["Tema", "Quantidade Registrada"]
                    print("\n" + tabela_formatada(cabecalhos, resultados))

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()
            
            # contagem por mes/ano
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

            # media mes/ano
            elif acao == 5:
                print("\n--- Relatório: Média de Materiais por Mês ---")
                try:
                    conexao = conectar()
                    cursor = conexao.cursor()
                    
                    sql = """
                    SELECT AVG(Contagem) 
                    FROM (
                        SELECT COUNT(*) as Contagem
                        FROM materiais
                        GROUP BY SUBSTR(data, 4, 7)
                    )
                    """
                    
                    cursor.execute(sql)
                    media = cursor.fetchone()[0]
                    
                    if media is None:
                        print("\nNenhum material registrado para calcular a média.")
                    else:
                        print(f"\nA média de materiais registrados por mês é: {media:.2f}")

                except Exception as e:
                    print(f"\n{erro()} Erro ao gerar relatório: {e}")
                finally:
                    if 'conexao' in locals():
                        conexao.close()

            else:
                print(f"\n{erro()} Opção inválida.")

        except ValueError:
            print(f"\n{erro()} Entrada inválida. Digite um número.")