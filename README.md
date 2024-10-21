# Projeto de E-commerce

Este projeto é uma aplicação web de e-commerce para a venda de produtos eletrônicos, como smartphones, relógios e acessórios. A aplicação é construída usando o framework Django.


## Estrutura de Diretórios

A estrutura de diretórios do projeto é organizada da seguinte forma:


## Descrição dos Arquivos

### `views.py`

Este arquivo contém as funções de visualização que controlam o comportamento das páginas da web. Cada função corresponde a uma página específica do site, como a página inicial, a loja, o carrinho de compras, o checkout, a conta do usuário e a página de login.

### `models.py`

Este arquivo define os modelos de dados usados na aplicação, representando as tabelas do banco de dados. Os principais modelos incluem Cliente, Categoria, Tipo, Produto, ItemEstoque, Endereco, Pedido, ItensPedido e Banner.

### `apps.py`

Este arquivo configura o aplicativo Django, definindo o nome do aplicativo e outras configurações padrão.

### `manage.py`

Este arquivo é a interface de linha de comando para interagir com o projeto Django. Ele permite executar comandos administrativos, como iniciar o servidor de desenvolvimento, aplicar migrações de banco de dados e criar novos aplicativos.

## Configuração do Ambiente de Desenvolvimento

### Passo 1: Clonar o Repositório

Clone o repositório do projeto para o seu ambiente local e navegue até o diretório do projeto.

### Passo 2: Criar e Ativar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto e ative-o. No macOS/Linux, use o comando `source` para ativar o ambiente. No Windows, use o comando `.\venv\Scripts\activate`.

### Passo 3: Instalar Dependências

Instale todas as dependências necessárias listadas no arquivo `requirements.txt` usando o comando `pip install -r requirements.txt`.

### Passo 4: Aplicar Migrações

Aplique as migrações para configurar o banco de dados com as tabelas definidas nos modelos. Use os comandos `makemigrations` e `migrate`.


### Passo 5: Exportar e Importar Dados no Django

O Django fornece ferramentas para gerenciar dados em seu banco de dados. Os comandos `dumpdata` e `loaddata` permitem exportar e importar dados de maneira simples e eficiente, facilitando a migração de dados entre ambientes ou o compartilhamento de dados entre desenvolvedores. Para exportar dados do seu banco de dados, use o comando `dumpdata`. Este comando gera um arquivo no formato JSON, XML ou YAML que contém todos os dados dos modelos do seu projeto.

- Sintaxe

```bash
#no terminal:
#Salva todos os dados do banco em um json
python manage.py dumpdata --output=all_data.json

#Em outra maquina, carrega todos os dados do json no banco.
python manage.py loaddata all_data.json

```

### Passo 6: Rodar o Servidor de Desenvolvimento

Inicie o servidor de desenvolvimento para testar a aplicação localmente. Use o comando `runserver`.

## Executando Testes

### Passo 1: Criar o Arquivo `pytest.ini`

Crie um arquivo `pytest.ini` na raiz do projeto para configurar o `pytest` com as configurações do Django.

### Passo 2: Rodar os Testes

Execute os testes automatizados para garantir que todas as funcionalidades estão funcionando corretamente. Use o comando `pytest`.


## Contribuindo

1. Faça um fork do projeto.
2. Crie uma nova branch para a sua feature ou correção.
3. Commit suas mudanças com uma mensagem descritiva.
4. Faça um push para a branch criada.
5. Crie um novo Pull Request para revisão.

---


