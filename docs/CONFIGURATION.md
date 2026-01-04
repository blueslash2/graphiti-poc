# Graphiti远程服务配置指南

## 环境变量配置

### 必需配置
```bash
# Graphiti服务地址（必填）
GRAPHITI_SERVICE_URL=http://your-remote-server:8000

# API密钥（如果服务启用认证）
GRAPHITI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 可选配置
```bash
# HTTP超时时间（秒），默认120
SERVICE_TIMEOUT=120

# 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=INFO

# 重试次数
MAX_RETRIES=3
```

## 服务健康检查
```bash
curl -X GET http://your-remote-server:8000/health \
  -H "Authorization: Bearer $GRAPHITI_API_KEY"
```
预期响应：
```JSON
{
  "status": "healthy",
  "neo4j": "connected",
  "ollama": "available",
  "version": "0.3.0"
}
```

## 安全配置建议

1. **生产环境务必启用HTTPS**
```bash
GRAPHITI_SERVICE_URL=https://your-domain.com
```
2. **使用专用API密钥**
- 在GitHub仓库设置中，将GRAPHITI_API_KEY添加到Secrets
- 本地开发使用.env文件（已加入.gitignore）
3. **IP白名单**
建议将服务端Neo4j和Ollama配置为仅接受Graphiti服务所在IP的连接

## 常见问题
**Q: 连接被拒绝？**
```bash
# 检查服务端口
telnet your-remote-server 8000

# 检查防火墙
sudo ufw allow 8000/tcp  # Ubuntu
```
**Q: 认证失败？**
- 确认Token格式：Authorization: Bearer <token>
- 检查Token是否过期（如果服务使用JWT）