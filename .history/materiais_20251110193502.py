from database import conectar
from formatacoes import ler_entrada, aviso_cancelar, erro
import sqlite3
from datetime import datetime

# --- Função Principal de Registro ---
def registrar_materiais():
    print("\n=== REGISTRAR MATERIAL ===")
    print(aviso_cancelar())
    # 2. Conexão com o Banco de Dados
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # 3. Coletar Entradas do Usuário
        titulo = ler_entrada("\nTítulo: ", str)
        if titulo is None: return

        # --- Validação para 'tipo' ---
        tipos_validos = ['artigo', 'vídeo', 'livro', 'curso', 'podcast']
        tipos_exibicao = [t.capitalize() for t in tipos_validos]
        while True:
            tipo_prompt = f"\nTipo ({', '.join(tipos_exibicao)}): "
            tipo = ler_entrada(tipo_prompt, str)
            if tipo is None: return
            if tipo.lower() in tipos_validos:
                tipo = tipo.lower()
                break
            else:
                print(f"\n{erro()} Tipos inválidos! Escolha um dos tipos da lista.")
        # --- Validação para 'nível' ---
        niveis_validos = ['básico', 'intermediário', 'avançado']
        niveis_exibicao = [n.capitalize() for n in niveis_validos]
        while True:
            niveis_prompt = f"\nNível ({', '.join(niveis_exibicao)}): "
            nivel = ler_entrada(niveis_prompt, str)
            if nivel is None: return
            if nivel.lower() in niveis_validos:
                nivel = nivel.lower()
                break
            else:
                print(f"\n{erro()} Níveis inválidos! Escolha um dos níveis da lista.")
                print(f"\n{erro()} Níveis inválidos! Escolha um dos níveis da lista.")
    except sqlite3.Error as e:
        print(f"\n{erro()} Erro no banco de dados: {e}")
        return
    except Exception as e:
        print(f"\n{erro()} Ocorreu um erro: {e}")
        return
    finally:
        try:
            if 'conexao' in locals() and conexao:
                conexao.close()
        except Exception:
            pass