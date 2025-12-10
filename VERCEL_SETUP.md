# 🚀 Guia de Configuração - Vercel

## ⚠️ IMPORTANTE: Variáveis de Ambiente

A API **NÃO VAI FUNCIONAR** sem as variáveis de ambiente corretas na Vercel.

## 📋 Checklist de Configuração

### 1. Acesse as configurações da Vercel
```
https://vercel.com/abraao-santos-projects/task-manager/settings/environment-variables
```

### 2. Adicione TODAS estas variáveis:

#### 🗄️ Database (Railway)
```
DB_HOST = seu-host.railway.app
DB_PORT = 3306
DB_NAME = railway
DB_USER = root
DB_PASSWORD = sua_senha_do_railway
```

**Como pegar do Railway:**
1. Acesse seu projeto no Railway
2. Vá em "Connect" → "MySQL"
3. Copie as credenciais exibidas

#### 🔐 JWT
```
JWT_SECRET_KEY = gere_uma_chave_aleatoria_aqui
JWT_ALGORITHM = HS256
JWT_EXPIRATION_HOURS = 24
```

**Como gerar JWT_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### ⚙️ Flask
```
FLASK_ENV = production
FLASK_DEBUG = False
PORT = 5000
```

#### 🔒 Security
```
BCRYPT_ROUNDS = 12
```

### 3. Configure para todos os ambientes
- ✅ **Production** (obrigatório)
- ✅ **Preview** (recomendado)
- ⬜ **Development** (opcional)

### 4. Salve e Redeploy
Após adicionar as variáveis:
```bash
vercel --prod
```

## 🧪 Teste a API

### Health Check
```bash
curl https://task-manager-k4onyhud7-abraao-santos-projects.vercel.app/api
```

Resposta esperada:
```json
{
  "success": true,
  "message": "Task Manager API is running",
  "version": "2.0.0"
}
```

### Teste Banco de Dados
```bash
curl https://task-manager-k4onyhud7-abraao-santos-projects.vercel.app/api/health/database
```

### Keep-Alive
```bash
curl https://task-manager-k4onyhud7-abraao-santos-projects.vercel.app/api/keep-alive/ping
```

## 🔧 Troubleshooting

### Erro: "Database connection failed"
- ✅ Verifique se todas as variáveis DB_* estão configuradas
- ✅ Confirme que o Railway está ativo e acessível
- ✅ Teste conexão local com as mesmas credenciais

### Erro: CORS
- ✅ CORS está configurado para aceitar todas as origens (*)
- ✅ Verifique se a URL do frontend está correta
- ✅ Confirme que está acessando `/api/...` nos endpoints

### Erro 404
- ✅ Verifique se a URL da API está correta no frontend
- ✅ URL deve incluir `/api` no final
- ✅ Exemplo correto: `https://sua-api.vercel.app/api`

### Erro 500
- ✅ Verifique logs na Vercel Dashboard
- ✅ Confirme que JWT_SECRET_KEY está definido
- ✅ Teste endpoint `/api/health/database`

## 📱 Frontend - Atualize a URL

No arquivo `task-app/js/config.js`:

```javascript
BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://task-manager-k4onyhud7-abraao-santos-projects.vercel.app/api',
```

## 🔄 Comandos Úteis

### Deploy
```bash
vercel --prod
```

### Ver logs
```bash
vercel logs
```

### Ver variáveis
```bash
vercel env ls
```

### Adicionar variável
```bash
vercel env add DB_HOST
```

## ✅ Checklist Final

- [ ] Todas as variáveis de ambiente configuradas na Vercel
- [ ] Railway database ativo e acessível
- [ ] Deploy feito com sucesso (sem erros)
- [ ] Teste `/api` retorna JSON correto
- [ ] Teste `/api/health/database` conecta ao banco
- [ ] Frontend tem URL correta da API
- [ ] CORS funcionando (sem erros no console)
- [ ] Consegue fazer login/registro

---

## 🎉 Tudo funcionando?

Seu Task Manager está pronto para uso!

### URLs importantes:
- **API**: https://task-manager-k4onyhud7-abraao-santos-projects.vercel.app/api
- **Frontend**: https://seu-usuario.github.io/task-app/login.html
- **Docs**: Veja README.md e KEEP_ALIVE.md

### Próximos passos:
1. Configure cron job para keep-alive (veja KEEP_ALIVE.md)
2. Publique frontend no GitHub Pages
3. Teste todas as funcionalidades
4. Configure domínio customizado (opcional)
