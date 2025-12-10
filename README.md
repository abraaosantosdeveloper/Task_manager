# Task Manager API

API REST completa para gerenciamento de tarefas com autenticação JWT.

## 🚀 Tecnologias

- **Flask 3.0.0** - Framework web
- **MySQL 9.4.0** - Banco de dados
- **JWT** - Autenticação
- **bcrypt** - Hash de senhas
- **Flask-CORS** - CORS habilitado

## 📡 Endpoints

### Autenticação
- `POST /api/auth/register` - Cadastro de usuário
- `POST /api/auth/login` - Login e geração de token
- `GET /api/auth/me` - Dados do usuário autenticado
- `PUT /api/auth/profile` - Atualizar perfil

### Tarefas
- `GET /api/tasks` - Listar todas as tarefas
- `POST /api/tasks` - Criar nova tarefa
- `GET /api/tasks/:id` - Buscar tarefa por ID
- `PUT /api/tasks/:id` - Atualizar tarefa
- `PUT /api/tasks/:id/status` - Atualizar status
- `DELETE /api/tasks/:id` - Deletar tarefa

### Keep-Alive (Sem autenticação)
- `GET /api/keep-alive/ping` - Manter banco de dados ativo
- `GET /api/keep-alive/health` - Health check

## 🔧 Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/abraaosantosdeveloper/Task_manager.git
cd Task_manager
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
Crie arquivo `.env`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=task_manager
DB_PORT=3306
JWT_SECRET_KEY=sua_chave_secreta_aqui
```

### 5. Crie o banco de dados
```bash
mysql -u root -p < database.sql
```

### 6. Execute a API
```bash
python index.py
```

API rodando em: `http://localhost:5000`

## 🌐 Deploy na Vercel

1. Configure variáveis de ambiente na Vercel
2. Conecte o repositório GitHub
3. Deploy automático!

## 🔄 Keep-Alive para Railway

Para evitar que o banco de dados do Railway "durma":

1. Execute `add_dummy_table.sql` no Railway
2. Configure um cron job apontando para:
   ```
   https://sua-api.vercel.app/api/keep-alive/ping
   ```
3. Intervalo recomendado: 10 minutos

📖 **[Ver documentação completa do Keep-Alive](KEEP_ALIVE.md)**

## 📁 Estrutura do Projeto

```
Task_manager/
├── api/
│   ├── controllers/      # Lógica de controle HTTP
│   ├── workers/          # Regras de negócio
│   ├── repositories/     # Acesso ao banco de dados
│   ├── middleware/       # Autenticação JWT
│   ├── routes/           # Definição de rotas
│   └── utils/            # Utilitários (config, db, responses)
├── index.py              # Entry point
├── database.sql          # Schema do banco
├── requirements.txt      # Dependências
└── vercel.json          # Configuração Vercel
```

## 🔐 Segurança

- ✅ Senhas com bcrypt
- ✅ JWT com expiração
- ✅ Validação de inputs
- ✅ CORS configurado
- ✅ Connection pooling
- ✅ Error handling

## 📝 Licença

MIT License
