from banco import senha_confere


class ErroLogin(Exception):
    pass


def efetuar_login(conexao, login, senha):
    login = (login or "").strip()

    if not login or not senha:
        raise ErroLogin("Informe o usuario e a senha.")

    usuario = conexao.execute(
        "SELECT id, nome, login, senha, perfil, ativo "
        "FROM usuario WHERE login = ?",
        (login,),
    ).fetchone()

    # Mesma mensagem para usuario inexistente e senha errada
    # (nao revela qual dos dois falhou)
    if usuario is None or not senha_confere(senha, usuario["senha"]):
        raise ErroLogin("Usuario ou senha incorretos.")

    if not usuario["ativo"]:
        raise ErroLogin("Conta desativada. Procure o proprietario.")

    return {
        "id": usuario["id"],
        "nome": usuario["nome"],
        "login": usuario["login"],
        "perfil": usuario["perfil"],
    }