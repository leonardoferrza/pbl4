import sqlite3

def criar_banco():
    conexao = sqlite3.connect("sge.db") 
    cursor = conexao.cursor()

    # 1. Tabela de Usuário
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    """)

    # 2. Tabela Principal de Materiais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL, 
        nivel TEXT NOT NULL,
        data TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        palavras_chave TEXT,
        
        id
    )
    """)
    # O 'UNIQUE' no 'link' impede materiais duplicados

    # 2. NOVA Tabela de Temas (Esta é a tabela que vai guardar a hierarquia)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_pai INTEGER,
        FOREIGN KEY (id_pai) REFERENCES temas(id)
    )""")
    
    conexao.commit() 
    conexao.close()  

def conectar():
    return sqlite3.connect("sge.db")