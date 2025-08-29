# User Manager API

Uma API REST moderna para gerenciamento de usuários construída com FastAPI, SQLAlchemy e autenticação JWT. Esse projeto foi inspirado no projeto do curso **[FastAPI](https://fastapidozero.dunossauro.com/)** do Eduardo Mendes (@dunossauro)

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)

## 🚀 Funcionalidades

- ✅ **CRUD completo de usuários**
- 🔐 **Autenticação JWT** com refresh token
- 🛡️ **Autorização baseada em permissões**
- 📊 **Paginação** de resultados
- 🐳 **Containerização** com Docker
- 🧪 **Cobertura de testes** completa
- 🔄 **CI/CD** com GitHub Actions
- 📚 **Documentação automática** com Swagger/ReDoc
- 🗄️ **Migrações de banco** com Alembic

## 📋 Tecnologias

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM assíncrono
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrações de banco
- **[Pydantic](https://pydantic.dev/)** - Validação de dados
- **[JWT](https://pyjwt.readthedocs.io/)** - Autenticação stateless
- **[Pwdlib](https://github.com/frankie567/pwdlib)** - Hash de senhas seguro

### Banco de Dados
- **PostgreSQL** (produção)
- **SQLite** (desenvolvimento/testes)

### DevOps
- **[Docker](https://www.docker.com/)** & **Docker Compose**
- **[Poetry](https://python-poetry.org/)** - Gerenciamento de dependências
- **[Ruff](https://github.com/astral-sh/ruff)** - Linting e formatação
- **[Pytest](https://pytest.org/)** - Framework de testes
- **GitHub Actions** - CI/CD

## 🏗️ Arquitetura

```
src/app/
├── routers/          # Endpoints da API
├── services/         # Lógica de negócio
├── repositories/     # Acesso a dados
├── models/           # Modelos SQLAlchemy
├── schemas/          # Schemas Pydantic
├── security/         # Autenticação & Autorização
├── database/         # Configuração do banco
├── dependencies/     # Injeção de dependência
└── settings/         # Configurações da aplicação
```

## 🚦 Início Rápido

### Pré-requisitos

- Python 3.13+
- Poetry
- Docker (opcional)

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/user-manager.git
cd user-manager
```

### 2. Instalação com Poetry

```bash
# Instalar Poetry (se não tiver)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite+aiosqlite:///./database.db
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Executar Migrações

```bash
poetry run alembic upgrade head
```

### 5. Iniciar o Servidor

```bash
# Desenvolvimento
poetry run task run

# Ou diretamente
poetry run fastapi dev src/app/app.py
```

A API estará disponível em: http://localhost:8000

## 🐳 Docker

### Docker Compose (Recomendado)

```bash
# Subir todos os serviços
docker compose up -d

# Ver logs
docker compose logs -f

# Parar serviços
docker compose down
```

### Docker Manual

```bash
# Build
docker build -t user-manager .

# Run
docker run -p 8000:8000 user-manager
```

## 🧪 Testes

```bash
# Executar todos os testes
poetry run task test

# Testes com coverage
poetry run pytest --cov=src/app --cov-report=html

# Executar testes específicos
poetry run pytest tests/test_auth.py -v
```

### Relatório de Coverage

Após executar os testes, abra `htmlcov/index.html` para ver o relatório de cobertura detalhado.

## 📚 Documentação da API

Com o servidor rodando, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/users/` | Criar usuário | ❌ |
| `GET` | `/users/` | Listar usuários | ✅ |
| `GET` | `/users/{id}` | Obter usuário por ID | ✅ |
| `PUT` | `/users/{id}` | Atualizar usuário | ✅ |
| `DELETE` | `/users/{id}` | Deletar usuário | ✅ |
| `POST` | `/auth/login` | Fazer login | ❌ |
| `POST` | `/auth/refresh_token` | Renovar token | ✅ |

## 🔐 Autenticação

### 1. Criar Usuário

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com", 
       "password": "secret123"
     }'
```

### 2. Fazer Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john@example.com&password=secret123"
```

### 3. Usar Token

```bash
curl -X GET "http://localhost:8000/users/" \
     -H "Authorization: Bearer seu-jwt-token-aqui"
```

## 🔧 Scripts Disponíveis

```bash
# Linting e formatação
poetry run task lint          # Verificar código
poetry run task format        # Formatar código

# Testes
poetry run task test          # Executar testes
poetry run task post_test     # Gerar relatório HTML

# Desenvolvimento  
poetry run task run           # Iniciar servidor dev
```

## 🚀 Deploy

### Variáveis de Ambiente para Produção

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/database
SECRET_KEY=sua-chave-super-secreta-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Comandos Úteis

```bash
# Gerar nova migração
poetry run alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrações
poetry run alembic upgrade head

# Voltar migração
poetry run alembic downgrade -1
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Desenvolvimento

- Siga as convenções do **Ruff**
- Escreva testes para novas funcionalidades
- Mantenha a cobertura de testes acima de 80%
- Use **Conventional Commits** para mensagens

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Raniere**
- Email: chownrani@proton.me
- GitHub: [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- [FastAPI do Zero](https://fastapidozero.dunossauro.com/) - Curso que inspirou este projeto
- Comunidade Python pela excelente documentação
- Todos os contribuidores open-source

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

## 📊 Status do Projeto

![Build Status](https://github.com/seu-usuario/user-manager/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/seu-usuario/user-manager/branch/main/graph/badge.svg)

**Versão Atual**: 1.0.0  
**Status**: ✅ Estável  
**Última Atualização**: Agosto 2025

