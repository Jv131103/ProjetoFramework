# Projeto do CRUD

# Por quê usamos o Flask:
    - Aqui estão alguns ótimos motivos para usar o Flask como framework web para o nosso projeto do semestre:
        1 - Micro Framework: O Flask é conhecido por ser um micro framework, o que significa que oferece apenas o básico necessário para criar aplicações web. Isso permite flexibilidade para escolher as ferramentas e bibliotecas que você deseja usar, evitando a sobrecarga de recursos desnecessários.

        2 - Simplicidade: A abordagem simples e minimalista do Flask torna mais fácil para os desenvolvedores entenderem e implementarem seus aplicativos. Ele oferece uma estrutura intuitiva e uma curva de aprendizado suave para iniciantes.

        3 - Extensibilidade: O Flask permite que você adicione facilmente extensões para adicionar funcionalidades específicas ao seu aplicativo. Existem várias extensões disponíveis, desde gerenciamento de formulários até autenticação e muito mais.

        4 - Flexibilidade: O Flask não impõe um padrão de projeto rígido, o que lhe dá a liberdade de escolher como organizar seus arquivos e estrutura de código de acordo com suas preferências ou necessidades do projeto.

        5 - Renderização de Templates: O Flask inclui um mecanismo de renderização de templates Jinja2 que facilita a criação de páginas HTML dinâmicas e reutilizáveis. Isso ajuda a manter a separação entre lógica de negócios e apresentação.

        6 - Rotas Simples: A definição de rotas no Flask é direta, permitindo que você associe URLs a funções específicas com facilidade. Isso torna a criação de endpoints de API ou páginas da web uma tarefa simples.

        7 - Suporte a RESTful APIs: Nosso projeto demonstra a criação de uma API RESTful para executar operações CRUD. O Flask é excelente para criar APIs, pois oferece controle sobre os métodos HTTP, facilitando a criação de serviços web eficientes.

        8 - Comunidade Ativa: O Flask possui uma comunidade ativa de desenvolvedores e uma ampla gama de recursos, tutoriais e documentação disponíveis online. Isso facilita a resolução de problemas e a obtenção de ajuda quando necessário.

        9 - Bom para Projetos Pequenos e Médios: Se o seu projeto não requer a complexidade de um grande framework, o Flask é uma escolha perfeita. Ele é ideal para projetos pequenos a médios nos quais você deseja manter a simplicidade e flexibilidade.

        10 - Adoção por Grandes Empresas: Apesar de ser um micro framework, o Flask é adotado por muitas empresas, grandes e pequenas, devido à sua eficácia na construção de aplicativos web eficientes e escaláveis. Alguns EX: (NASA, NetFlix, Reddit, Mozilla e Pinterest)
            - Lembrando que esses são apenas exemplos e não necessariamente a escolha única para todos os projetos dessas empresas. O Flask é valorizado por sua simplicidade, flexibilidade e rapidez de desenvolvimento, o que o torna uma opção atraente para empresas que precisam criar aplicativos web eficientes em um curto espaço de tempo.

Em resumo, escolhemos usar o Flask por sua simplicidade, flexibilidade e capacidade de criar tanto aplicativos web tradicionais quanto APIs RESTful. Nossa escolha reflete bem o escopo do projeto e suas necessidades específicas.

Este é um projeto simples que demonstra uma aplicação web construída com Flask, envolvendo uma classe de conector para um banco de dados MySQL. A aplicação permite o registro e autenticação de usuários, além de operações CRUD (Create, Read, Update, Delete) em relação a registros de usuários no banco de dados. As classes `Conector` e `VerificacaoCrud` encapsulam as operações de banco de dados.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados antes de executar este projeto:

- Python (versão utilizada: 3.7+)
- Biblioteca MySQL Connector (`pip install mysql-connector-python`)
- Biblioteca Flask (`pip install Flask`)
- Biblioteca Flask-MySQL (`pip install Flask-MySQL`)

## Configuração

1. Crie um banco de dados MySQL com o nome "Projeto" ou ajuste o nome do banco no código conforme necessário.

2. Abra o arquivo `view.py` e configure as credenciais do banco de dados (`MYSQL_DATABASE_USER`, `MYSQL_DATABASE_PASSWORD`, `MYSQL_DATABASE_DB`).

    - OBS: Já possuimos o banco, se quiser não percisa recriar, só utilizar o nosso banco mesmo!
    - Pode pular os passos 1 e 2

3. Execute o arquivo `view.py` para iniciar o servidor Flask.

## Uso

A aplicação web inclui as seguintes funcionalidades:

- **Registro de Usuário:** Preencha o formulário de registro para criar uma conta. O sistema verifica se o e-mail ou CPF já foram cadastrados anteriormente.

- **Autenticação de Usuário:** Faça login com suas credenciais de e-mail e senha.

- **Lista de Usuários:** Visualize uma lista de todos os usuários registrados no banco de dados.

- **Detalhes do Usuário:** Obtenha detalhes específicos de um usuário com base no ID.

- **Atualização de Usuário:** Atualize os detalhes de um usuário existente.

- **Exclusão de Usuário:** Exclua um usuário do banco de dados.

## Exemplos de Uso

### Páginas Web

Você pode acessar a aplicação web em `http://localhost:5001`.

- Acesse `http://localhost:5001` para visualizar a página de login.

- Acesse `http://localhost:5001/gravar` para visualizar a página de cadastro.

- Acesse `http://localhost:5001/listar` para visualizar a lista de usuários.

### APIs

As rotas API estão disponíveis em `http://localhost:5002/cadastro/api`.

- **`POST /cadastro/api/insert`**: Crie um novo usuário. Envie os dados do usuário no corpo da solicitação como um JSON.

- **`GET /cadastro/api/read`**: Leia todos os usuários registrados.

- **`GET /cadastro/api/read/<int:id>`**: Leia os detalhes de um usuário específico com base no ID.

- **`PUT /cadastro/api/update/<int:id>`**: Atualize os detalhes de um usuário existente. Envie os novos dados do usuário no corpo da solicitação como um JSON.

- **`DELETE /cadastro/api/delete/<int:id>`**: Exclua um usuário do banco de dados com base no ID.

- **`GET /cadastro/api/ativar/<int:id>`

## Contribuição

Contribuições são bem-vindas! Se você encontrar algum problema, tiver uma ideia para melhoria ou quiser adicionar novos recursos, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## Licença

Este projeto é licenciado sob a [Licença MIT](LICENSE).

---

OBS: Se quiser baixar nosso projeto completo, pegue o arquivo ProjetoCompleto.zip, extraia ele e obterá o acesso ao nosso
código fonte completo
