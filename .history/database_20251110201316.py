import sqlite3

def criar_banco():
    # Conecta ao banco (ou cria se não existir)
    conexao = sqlite3.connect("sge.db") 
    cursor = conexao.cursor()

    # 1. Tabela de Usuário (copiada do PBL3 [cite: 46-50], mas mais simples)
    # Removemos o 'saldo_atual' que não precisamos mais.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    """)

    # 2. Tabela Principal de Materiais (aqui fica quase tudo)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL, 
        nivel TEXT NOT NULL,
        data TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        
        palavras_chave TEXT,
        
        tema_1 TEXT,
        tema_2 TEXT,
        tema_3 TEXT,
        tema_4 TEXT,
        tema_5 TEXT
    )
    """)
    # O 'UNIQUE' no 'link' impede materiais duplicados
    
    conexao.commit() # Salva as alterações
    conexao.close()  # Fecha a conexão

def conectar():
    return sqlite3.connect("sge.db")