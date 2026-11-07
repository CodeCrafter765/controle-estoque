import sqlite3


class ErroProduto(Exception):
    pass


def listar_categorias(conexao):
    return conexao.execute("SELECT id, nome FROM categoria ORDER BY nome").fetchall()


def cadastrar_produto(conexao, usuario, nome, codigo, categoria_id, preco,
                      quantidade_inicial, quantidade_minima):
    
    if usuario is None or usuario["perfil"] != "proprietario":
        raise ErroProduto("Apenas o proprietario pode cadastrar produtos.")

    nome = (nome or "").strip()
    codigo = (codigo or "").strip()
    if not nome or not codigo:
        raise ErroProduto("Nome e codigo sao obrigatorios.")

    try:
        preco = float(str(preco).replace(",", "."))
        quantidade_inicial = int(quantidade_inicial)
        quantidade_minima = int(quantidade_minima)
        categoria_id = int(categoria_id)
    except (TypeError, ValueError):
        raise ErroProduto("Preco e quantidades devem ser numeros validos.")

    if preco < 0 or quantidade_inicial < 0 or quantidade_minima < 0:
        raise ErroProduto("Preco e quantidades nao podem ser negativos.")

    if conexao.execute("SELECT 1 FROM categoria WHERE id = ?", (categoria_id,)).fetchone() is None:
        raise ErroProduto("Categoria inexistente.")

    try:
        cursor = conexao.execute(
            """INSERT INTO produto
               (codigo, nome, preco, quantidade_atual, quantidade_minima, categoria_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (codigo, nome, preco, quantidade_inicial, quantidade_minima, categoria_id),
        )
        conexao.commit()
    except sqlite3.IntegrityError:
        conexao.rollback()
        raise ErroProduto(f"Ja existe um produto cadastrado com o codigo '{codigo}'.")
    return cursor.lastrowid


def consultar_produtos(conexao, termo=""):
    busca = f"%{(termo or '').strip()}%"
    return conexao.execute(
        """SELECT p.codigo, p.nome, c.nome AS categoria, p.preco,
                  p.quantidade_atual, p.quantidade_minima
           FROM produto p JOIN categoria c ON c.id = p.categoria_id
           WHERE p.nome LIKE ? OR p.codigo LIKE ?
           ORDER BY p.nome""",
        (busca, busca),
    ).fetchall()
