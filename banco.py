import hashlib
import os
import sqlite3

ARQUIVO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estoque.db")


def conectar(caminho=None):
    conexao = sqlite3.connect(caminho or ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def gerar_hash_senha(senha, salt=None):
    salt = salt or os.urandom(16).hex()
    hash_ = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), bytes.fromhex(salt), 100_000)
    return f"{salt}${hash_.hex()}"


def senha_confere(senha, armazenada):
    salt, _ = armazenada.split("$")
    return gerar_hash_senha(senha, salt) == armazenada


def criar_tabelas(conexao):
    conexao.executescript("""
    CREATE TABLE IF NOT EXISTS usuario (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        nome    TEXT    NOT NULL,
        login   TEXT    NOT NULL UNIQUE,
        senha   TEXT    NOT NULL,
        perfil  TEXT    NOT NULL CHECK (perfil IN ('proprietario', 'funcionario')),
        ativo   INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS categoria (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        nome      TEXT NOT NULL UNIQUE,
        descricao TEXT
    );

    CREATE TABLE IF NOT EXISTS produto (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo            TEXT    NOT NULL UNIQUE,
        nome              TEXT    NOT NULL,
        preco             REAL    NOT NULL CHECK (preco >= 0),
        quantidade_atual  INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_atual >= 0),
        quantidade_minima INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_minima >= 0),
        categoria_id      INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categoria (id)
    );

    CREATE TABLE IF NOT EXISTS movimentacao (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo        TEXT    NOT NULL CHECK (tipo IN ('entrada', 'saida')),
        quantidade  INTEGER NOT NULL CHECK (quantidade > 0),
        data_hora   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
        usuario_id  INTEGER NOT NULL,
        produto_id  INTEGER NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario (id),
        FOREIGN KEY (produto_id) REFERENCES produto (id)
    );
    """)
    conexao.commit()


def popular_dados_iniciais(conexao):
    if conexao.execute("SELECT COUNT(*) FROM usuario").fetchone()[0] == 0:
        usuarios = [
            ("Dono da Loja", "admin", "admin123", "proprietario", 1),
            ("Funcionario Teste", "func", "func123", "funcionario", 1),
            ("Funcionario Inativo", "inativo", "inativo123", "funcionario", 0),
        ]
        for nome, login, senha, perfil, ativo in usuarios:
            conexao.execute(
                "INSERT INTO usuario (nome, login, senha, perfil, ativo) VALUES (?, ?, ?, ?, ?)",
                (nome, login, gerar_hash_senha(senha), perfil, ativo),
            )
    if conexao.execute("SELECT COUNT(*) FROM categoria").fetchone()[0] == 0:
        for nome, descricao in [
            ("Papelaria", "Cadernos, canetas e materiais escolares"),
            ("Utilidades", "Utensilios domesticos em geral"),
            ("Brinquedos", "Brinquedos e jogos"),
            ("Higiene", "Produtos de limpeza e higiene"),
        ]:
            conexao.execute("INSERT INTO categoria (nome, descricao) VALUES (?, ?)", (nome, descricao))
    conexao.commit()


def iniciar_banco(caminho=None):
    conexao = conectar(caminho)
    criar_tabelas(conexao)
    popular_dados_iniciais(conexao)
    return conexao
