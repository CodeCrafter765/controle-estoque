# Sistema de Controle de Estoque - Loja de Variedades

Projeto Integrado (ADS)

## Como rodar
    python main.py        # abre o sistema (cria estoque.db sozinho na 1a vez)
    python testes.py      # roda os testes automatizados

## Usuarios de exemplo
| login   | senha      | perfil       |
|---------|------------|--------------|
| admin   | admin123   | proprietario |
| func    | func123    | funcionario  |
| inativo | inativo123 | funcionario (conta desativada) |

## Funcionalidades
1. UC01 - Efetuar login (autenticacao.py)
2. UC03 - Cadastrar produtos (produtos.py), com consulta (UC04) para exibir o resultado

## Arquivos
- banco.py: cria as 4 tabelas do MER e os dados iniciais
- autenticacao.py: logica do login
- produtos.py: cadastro e consulta de produtos
- main.py: telas de terminal
- testes.py: casos de teste

## Git
    git init
    git add .
    git commit -m "Fase 4 - login e cadastro de produtos"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/estoque.git
    git push -u origin main
