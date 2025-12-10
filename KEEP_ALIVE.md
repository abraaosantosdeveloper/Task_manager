# Keep-Alive Configuration

## 🎯 Objetivo

Evitar que o banco de dados do Railway "durma" por inatividade, fazendo requisições periódicas.

## 📡 Endpoints Disponíveis

### 1. `/api/keep-alive/ping` (Recomendado)
- **Método**: GET
- **Autenticação**: Não requer
- **Função**: Faz query na tabela `dummy_data` para manter o banco ativo
- **Resposta**:
```json
{
  "success": true,
  "message": "Database is active",
  "data": {
    "status": "alive",
    "dummy_data": {
      "id": 1,
      "is_active": true,
      "last_ping": "2025-12-10 03:30:00",
      "description": "Database keep-alive record"
    }
  }
}
```

### 2. `/api/keep-alive/health`
- **Método**: GET
- **Autenticação**: Não requer
- **Função**: Health check simples sem query no banco
- **Resposta**:
```json
{
  "success": true,
  "message": "API is running",
  "data": {
    "status": "healthy",
    "service": "Task Manager API",
    "version": "2.0.0"
  }
}
```

## 🔧 Configuração do Cron Job

### Opção 1: Cron-Job.org (Gratuito)

1. Acesse: https://cron-job.org/
2. Crie uma conta
3. Adicione um novo cron job:
   - **URL**: `https://sua-api.vercel.app/api/keep-alive/ping`
   - **Schedule**: A cada 10 minutos
   - **HTTP Method**: GET
   - **Timeout**: 30 segundos

### Opção 2: UptimeRobot (Gratuito)

1. Acesse: https://uptimerobot.com/
2. Crie uma conta
3. Adicione um novo monitor:
   - **Monitor Type**: HTTP(s)
   - **URL**: `https://sua-api.vercel.app/api/keep-alive/ping`
   - **Monitoring Interval**: 5 minutos (plano free)

### Opção 3: EasyCron (Gratuito)

1. Acesse: https://www.easycron.com/
2. Crie uma conta
3. Adicione um cron job:
   - **URL**: `https://sua-api.vercel.app/api/keep-alive/ping`
   - **Cron Expression**: `*/10 * * * *` (a cada 10 minutos)

### Opção 4: GitHub Actions (Gratuito)

Crie `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Database Alive

on:
  schedule:
    # Executa a cada 10 minutos
    - cron: '*/10 * * * *'
  workflow_dispatch: # Permite executar manualmente

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping API
        run: |
          curl -X GET https://sua-api.vercel.app/api/keep-alive/ping
```

## 📊 Tabela Dummy Data

### Estrutura
```sql
CREATE TABLE `dummy_data` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `last_ping` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `description` VARCHAR(255) DEFAULT 'Keep-alive ping data'
);
```

### Como criar
Execute o arquivo `add_dummy_table.sql` no Railway:

```bash
mysql -h <host> -u <user> -p <database> < add_dummy_table.sql
```

Ou execute manualmente no Railway Dashboard:

1. Acesse Railway → Seu projeto → Database
2. Vá em "Query"
3. Cole e execute o conteúdo de `add_dummy_table.sql`

## ✅ Verificação

### Teste manual
```bash
curl https://sua-api.vercel.app/api/keep-alive/ping
```

### Verifique o timestamp
O campo `last_ping` na tabela `dummy_data` deve ser atualizado a cada requisição.

```sql
SELECT * FROM dummy_data;
```

## 📈 Recomendações

- **Intervalo ideal**: 10-15 minutos
- **Evite intervalos muito curtos**: Pode gerar custos desnecessários
- **Monitore**: Use ferramentas que enviam alertas se o ping falhar
- **Backup**: Configure mais de um serviço de cron job

## 🚨 Troubleshooting

### Erro: "Database connection failed"
- Verifique se o banco Railway está ativo
- Confirme as credenciais no `.env`
- Teste a conexão manualmente

### Erro: "Table 'dummy_data' doesn't exist"
- Execute o arquivo `add_dummy_table.sql`
- Ou crie a tabela manualmente no Railway

### Ping não atualiza `last_ping`
- Verifique se o cron job está ativo
- Confirme a URL do endpoint
- Teste manualmente com `curl`

---

## 📝 Notas

- Endpoint **público** (sem autenticação)
- Leve e rápido (< 100ms)
- Não afeta performance da API
- Compatible com qualquer serviço de cron/monitoring
