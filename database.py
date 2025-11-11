# Arquivo: PBL4/database.py (VERSÃO HIERÁRQUICA)

import sqlite3

def criar_banco():
    # Conecta ao banco (ou cria se não existir)
    conexao = sqlite3.connect("pbl4.db") 
    cursor = conexao.cursor()

    # 1. Tabela de Usuário (Sem mudanças)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )""")

    # 2. NOVA Tabela de Temas
    # Esta é a tabela que vai guardar a hierarquia
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_pai INTEGER,
        FOREIGN KEY (id_pai) REFERENCES temas(id)
    )""")

    # 3. Tabela Principal de Materiais (MODIFICADA)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        tipo TEXT NOT NULL, 
        nivel TEXT NOT NULL,
        data TEXT NOT NULL,
        link TEXT NOT NULL UNIQUE,
        palavras_chave TEXT,
        
        id_tema INTEGER,
        
        FOREIGN KEY (id_tema) REFERENCES temas(id)
    )""")
    
    conexao.commit() # Salva as alterações
    conexao.close()  # Fecha a conexão

def conectar():
    # Função simples para conectar ao banco
    return sqlite3.connect("pbl4.db")