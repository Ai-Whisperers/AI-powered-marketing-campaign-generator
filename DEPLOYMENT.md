# Production Deployment Guide

## Quick Start

Deploy MAGA to production in 4 steps:

```bash
# 1. Configure environment
cp .env.production.template .env.production
nano .env.production  # Edit with your values

# 2. Build and start services
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 3. Run database migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# 4. Verify deployment
curl http://localhost:8000/health
```

---

## Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Server** with 4GB+ RAM, 20GB+ disk
- **Domain** (optional, for SSL/HTTPS)

---

## Configuration

### 1. Environment Variables

Copy the template and configure:

```bash
cp .env.production.template .env.production
```

**Required variables:**
- `API_KEY` - Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `POSTGRES_PASSWORD` - Secure database password
- `OPENAI_API_KEY` - Your OpenAI API key
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `GOOGLE_API_KEY` - Your Google API key

**Optional variables:**
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

### 2. Secrets Management

**Production best practices:**

```bash
# Use environment variables (recommended)
export API_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
export POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Or use Docker secrets
echo "my-secure-password" | docker secret create postgres_password -
```

---

## Deployment

### Build Images

```bash
docker-compose -f docker-compose.prod.yml build
```

### Start Services

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f api
```

### Run Migrations

```bash
# Apply database migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Verify tables created
docker-compose -f docker-compose.prod.yml exec postgres psql -U maga_user -d maga_prod -c "\dt"
```

---

## Verification

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2025-11-23T19:00:00Z","service":"maga-api"}

# Database health
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U maga_user

# Redis health
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping
```

### Test API

```bash
# Create a project
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "name": "Test Campaign",
    "client": "Test Client",
    "country": "US",
    "language": "en",
    "campaign_type": "social"
  }'

# List projects
curl http://localhost:8000/api/projects
```

---

## Monitoring

### View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f api
docker-compose -f docker-compose.prod.yml logs -f celery-worker

# Last 100 lines
docker-compose -f docker-compose.prod.yml logs --tail=100 api
```

### Resource Usage

```bash
# Container stats
docker stats

# Disk usage
docker system df

# Database size
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U maga_user -d maga_prod -c "SELECT pg_size_pretty(pg_database_size('maga_prod'));"
```

---

## Maintenance

### Backup Database

```bash
# Create backup
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U maga_user maga_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U maga_user maga_prod | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore Database

```bash
# Restore from backup
cat backup_20251123.sql | docker-compose -f docker-compose.prod.yml exec -T postgres \
  psql -U maga_user -d maga_prod
```

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run new migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

---

## Troubleshooting

### API Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs api

# Common issues:
# 1. Database not ready - wait for postgres healthcheck
# 2. Missing environment variables - check .env.production
# 3. Port already in use - change port in docker-compose.prod.yml
```

### Database Connection Errors

```bash
# Verify database is running
docker-compose -f docker-compose.prod.yml ps postgres

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres

# Test connection
docker-compose -f docker-compose.prod.yml exec postgres \
  psql -U maga_user -d maga_prod -c "SELECT 1;"
```

### Celery Tasks Not Running

```bash
# Check celery worker logs
docker-compose -f docker-compose.prod.yml logs celery-worker

# Verify Redis connection
docker-compose -f docker-compose.prod.yml exec redis redis-cli ping

# Restart celery worker
docker-compose -f docker-compose.prod.yml restart celery-worker
```

---

## Security

### Production Checklist

- [ ] Change all default passwords
- [ ] Generate secure API keys
- [ ] Configure CORS allowed origins
- [ ] Enable HTTPS (use nginx reverse proxy)
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Regular security updates
- [ ] Backup strategy in place

### SSL/HTTPS Setup

Use nginx as reverse proxy:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Scaling

### Horizontal Scaling

```yaml
# In docker-compose.prod.yml
api:
  deploy:
    replicas: 3  # Run 3 API instances

celery-worker:
  deploy:
    replicas: 4  # Run 4 worker instances
```

### Resource Limits

```yaml
api:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
      reservations:
        cpus: '1'
        memory: 1G
```

---

## Support

For issues or questions:
1. Check logs: `docker-compose logs`
2. Review this guide
3. Check GitHub issues
4. Contact support

---

## Next Steps

After deployment:
1. Set up monitoring (Prometheus + Grafana)
2. Configure automated backups
3. Set up log aggregation
4. Implement CI/CD pipeline
5. Load testing
