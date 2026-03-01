# 🚀 LUMA - Sistema Completo de Gestão de Projetos e Tarefas

API RESTful robusta desenvolvida com **Flask + MySQL**, arquitetura em camadas (DAO, Service, Control, Middleware, Router) e autenticação JWT.

Projeto estruturado seguindo boas práticas de engenharia de software, separação de responsabilidades e injeção de dependência.

---

# 📑 Sumário

- [📌 Visão Geral](#-visão-geral)
- [🏗️ Arquitetura](#️-arquitetura)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [⚙️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [🔐 Autenticação JWT](#-autenticação-jwt)
- [📡 Endpoints da API](#-endpoints-da-api)
  - [🔑 Autenticação](#-autenticação)
  - [👤 Usuário](#-usuário)
  - [📁 Projeto](#-projeto)
  - [✅ Tarefa](#-tarefa)
- [❤️ Health Check](#-health-check)
- [📦 Como Executar](#-como-executar)
- [📊 Banco de Dados](#-banco-de-dados)
- [🧠 Diferenciais Técnicos](#-diferenciais-técnicos)

---

# 📌 Visão Geral

O **LUMA** é um sistema completo de gerenciamento de:

- 👤 Usuários
- 📁 Projetos
- ✅ Tarefas

Com:

- 🔐 Autenticação JWT
- 🧱 Arquitetura em camadas
- 🛡️ Middlewares de validação
- 📧 Sistema de recuperação de senha por e-mail
- 🔄 Pool de conexões MySQL
- 📊 Dashboard de estatísticas
- 🌐 Frontend estático integrado

---

# 🏗️ Arquitetura

Arquitetura organizada em camadas:

- **DAO** → Acesso ao banco de dados
- **Service** → Regras de negócio
- **Control** → Orquestração da lógica
- **Middleware** → Validações e autenticação
- **Router** → Definição de endpoints

Separação clara de responsabilidades.

---

# 📂 Estrutura do Projeto

```bash
LUMA/
├── app.py
├── server.py
├── install.py
├── README.md
│
├── api/
│   ├── control/
│   ├── dao/
│   ├── database/
│   ├── http/
│   ├── middleware/
│   ├── model/
│   ├── router/
│   ├── service/
│   ├── system/
│   └── utils/
│
├── docs/
│   └── Banco.sql
│
└── static/
    ├── dashboard.html
    ├── login.html
    ├── register.html
    ├── projeto.html
    ├── tarefa.html
    ├── usuario.html
```

---

# ⚙️ Tecnologias Utilizadas

- Python 3.x
- Flask
- MySQL
- JWT (Autenticação)
- Bootstrap
- JavaScript
- CORS configurado
- SMTP (recuperação de senha)

---

# 🔐 Autenticação JWT

Todas as rotas protegidas exigem:

```
Authorization: Bearer {token}
```

O token é gerado no login e validado via middleware.

---

# 📡 Endpoints da API

Base URL:

```
http://localhost:5000
```

---

# 🔑 Autenticação

## POST /api/usuario/login
Autentica usuário e retorna JWT.

## POST /api/auth/recuperar-senha
Envia e-mail com link de redefinição.

## POST /api/auth/redefinir-senha
Redefine senha via token.

## POST /api/usuario/logout
Logout do usuário autenticado.

---

# 👤 Usuário

Prefixo: `/api/usuario`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | / | Criar usuário |
| GET | / | Listar usuários |
| GET | /<id> | Buscar usuário |
| PUT | /<id> | Atualizar usuário |
| DELETE | /<id> | Remover usuário |
| GET | /me | Usuário autenticado |
| GET | /email/<email> | Buscar por email |
| GET | /verificar-email/<email> | Verificar se email existe |

---

# 📁 Projeto

Prefixo: `/api/projeto`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | / | Criar projeto |
| GET | / | Listar projetos do usuário |
| GET | /<id> | Buscar projeto |
| PUT | /<id> | Atualizar projeto |
| DELETE | /<id> | Remover projeto |
| GET | /usuario/<usuario_id> | Projetos por usuário |
| GET | /meus-projetos | Projetos do usuário autenticado |

---

# ✅ Tarefa

Prefixo: `/api/tarefa`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | / | Criar tarefa |
| GET | / | Listar tarefas (responsável) |
| GET | /<id> | Buscar tarefa |
| PUT | /<id> | Atualizar tarefa |
| DELETE | /<id> | Remover tarefa |
| GET | /projeto/<projeto_id> | Tarefas por projeto |
| PUT | /<id>/concluir | Concluir tarefa |
| PUT | /<id>/toggle-concluir | Alternar status |
| GET | /minhas-tarefas | Tarefas como responsável |
| GET | /atribuidas-por-mim | Tarefas atribuídas |
| GET | /dashboard | Estatísticas |
| GET | /todas-tarefas | Todas tarefas (dev/admin) |
| GET | /usuarios-disponiveis | Lista de usuários |
| GET | /health | Health check da tarefa |

---

# ❤️ Health Check

## GET /health

Verifica status da API e banco.

Resposta:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

# 📦 Como Executar

1. Clonar repositório

```
git clone https://github.com/Todeschiniii/LUMA.git
```

2. Instalar dependências

```
pip install -r requirements.txt
```

3. Criar banco MySQL

Execute:

```
docs/Banco.sql
```

4. Rodar aplicação

```
python app.py
```

API disponível em:

```
http://localhost:5000
```

---

# 📊 Banco de Dados

- Pool de conexões MySQL
- Reconexão automática
- Tratamento global de erros
- MockDatabase para fallback

---

# 🧠 Diferenciais Técnicos

- Arquitetura em camadas real
- Injeção de dependência
- JWT customizado
- Middlewares desacoplados
- Tratamento global de exceções
- Recuperação de senha com token temporário
- Sistema preparado para produção
- Organização profissional de código

---

# 👨‍💻 Autor

Mateus Todeschini  
Desenvolvedor Backend focado em arquitetura limpa, APIs robustas e boas práticas de engenharia de software.

---

# 📄 Licença

Projeto para fins educacionais e portfólio.

Repositório: https://github.com/Todeschiniii/LUMA
