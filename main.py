from autenticacao import ErroLogin, efetuar_login
from banco import iniciar_banco
from produtos import ErroProduto, cadastrar_produto, consultar_produtos, listar_categorias

LINHA = "=" * 62


def tela_login(conexao):
    while True:
        print(f"\n{LINHA}\n  CONTROLE DE ESTOQUE - LOJA DE VARIEDADES\n  LOGIN\n{LINHA}")
        login = input("Usuario (0 para sair): ").strip()
        if login == "0":
            return None
        senha = input("Senha: ")
        try:
            usuario = efetuar_login(conexao, login, senha)
        except ErroLogin as erro:
            print(f"\n[ERRO] {erro}")
            continue
        print(f"\n[OK] Bem-vindo(a), {usuario['nome']}! Perfil: {usuario['perfil']}.")
        return usuario


def tela_cadastro(conexao, usuario):
    print(f"\n{LINHA}\n  CADASTRO DE PRODUTO\n{LINHA}")
    print("Categorias disponiveis:")
    for cat in listar_categorias(conexao):
        print(f"  {cat['id']} - {cat['nome']}")
    nome = input("Nome: ")
    codigo = input("Codigo: ")
    categoria = input("Numero da categoria: ")
    preco = input("Preco (ex: 12,50): ")
    qtd_inicial = input("Quantidade inicial: ")
    qtd_minima = input("Quantidade minima: ")
    try:
        cadastrar_produto(conexao, usuario, nome, codigo, categoria, preco, qtd_inicial, qtd_minima)
        print("\n[OK] Produto cadastrado com sucesso!")
    except ErroProduto as erro:
        print(f"\n[ERRO] {erro}")


def tela_consulta(conexao):
    print(f"\n{LINHA}\n  CONSULTA DE PRODUTOS\n{LINHA}")
    termo = input("Buscar por nome ou codigo (Enter lista todos): ")
    produtos = consultar_produtos(conexao, termo)
    if not produtos:
        print("\nNenhum produto encontrado.")
        return
    print(f"\n{'Codigo':<10}{'Nome':<24}{'Categoria':<12}{'Preco':>9}{'Estoque':>9}{'Minimo':>8}")
    print("-" * 72)
    for p in produtos:
        print(f"{p['codigo']:<10}{p['nome']:<24}{p['categoria']:<12}"
              f"{p['preco']:>9.2f}{p['quantidade_atual']:>9}{p['quantidade_minima']:>8}")


def menu_principal(conexao, usuario):
    while True:
        print(f"\n{LINHA}\n  MENU PRINCIPAL  ({usuario['nome']} - {usuario['perfil']})\n{LINHA}")
        print("1 - Consultar produtos")
        if usuario["perfil"] == "proprietario":
            print("2 - Cadastrar produto")
        print("0 - Sair")
        opcao = input("Opcao: ").strip()
        if opcao == "1":
            tela_consulta(conexao)
        elif opcao == "2" and usuario["perfil"] == "proprietario":
            tela_cadastro(conexao, usuario)
        elif opcao == "0":
            return
        else:
            print("[ERRO] Opcao invalida.")


def main():
    conexao = iniciar_banco()
    usuario = tela_login(conexao)
    if usuario:
        menu_principal(conexao, usuario)
    conexao.close()
    print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
