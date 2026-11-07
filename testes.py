import unittest

from autenticacao import ErroLogin, efetuar_login
from banco import iniciar_banco
from produtos import ErroProduto, cadastrar_produto, consultar_produtos


class TestesEstoque(unittest.TestCase):
    def setUp(self):
        self.con = iniciar_banco(":memory:")
        self.dono = efetuar_login(self.con, "admin", "admin123")

    def novo(self, **kw):
        dados = dict(nome="Caderno", codigo="P001", categoria_id=1, preco="12,50",
                     quantidade_inicial=10, quantidade_minima=3)
        dados.update(kw)
        return cadastrar_produto(self.con, self.dono, **dados)

    # ---- UC01 ----
    def test_ct01_login_valido(self):
        self.assertEqual(self.dono["perfil"], "proprietario")

    def test_ct02_senha_incorreta(self):
        with self.assertRaises(ErroLogin):
            efetuar_login(self.con, "admin", "errada")

    def test_ct03_conta_desativada(self):
        with self.assertRaises(ErroLogin):
            efetuar_login(self.con, "inativo", "inativo123")

    def test_senha_nao_fica_em_texto_puro(self):
        senha = self.con.execute("SELECT senha FROM usuario WHERE login='admin'").fetchone()[0]
        self.assertNotIn("admin123", senha)

    # ---- UC03 ----
    def test_ct04_cadastro_valido(self):
        self.novo()
        self.assertEqual(len(consultar_produtos(self.con, "Caderno")), 1)

    def test_ct05_codigo_duplicado(self):
        self.novo()
        with self.assertRaises(ErroProduto):
            self.novo(nome="Outro")

    def test_ct06_valor_negativo(self):
        with self.assertRaises(ErroProduto):
            self.novo(preco="-5")

    def test_ct07_nome_vazio(self):
        with self.assertRaises(ErroProduto):
            self.novo(nome="  ")

    def test_ct08_funcionario_nao_cadastra(self):
        func = efetuar_login(self.con, "func", "func123")
        with self.assertRaises(ErroProduto):
            cadastrar_produto(self.con, func, "X", "X1", 1, "1", 1, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
