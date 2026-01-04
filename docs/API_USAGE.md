# Graphiti知识图谱API使用文档

## 🚀 快速开始

### 启动服务
```bash
# 使用uvicorn直接启动
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 或使用脚本入口
uv run graphiti-api
```

### 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 📖 API端点

### 添加文本情节
**POST** `/api/episodes/text`

将长文本内容添加为知识图谱中的情节节点。

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | ✅ | 长文本内容（最少1个字符） |
| description | string | ❌ | 描述信息，默认"文本信息" |
| name | string | ❌ | 情节名称，不传则自动生成 |
| reference_time | string | ❌ | 参考时间，格式：yyyyMMdd 或 yyyyMM |

#### 请求示例
```json
{
  "content": "张三是一名软件工程师，在北京的科技公司工作。他主要负责前端开发，使用React和TypeScript技术栈。",
  "description": "员工档案信息",
  "name": "张三档案",
  "reference_time": "20240104"
}
```

#### 响应格式
```json
{
  "success": true,
  "message": "文本情节添加成功",
  "data": {
    "name": "张三档案",
    "description": "员工档案信息",
    "content_preview": "张三是一名软件工程师，在北京的科技公司工作。他主要负责前端开发，使...",
    "reference_time": "20240104",
    "episode_type": "text"
  }
}
```

#### 使用示例
```bash
# 完整参数
curl -X POST "http://localhost:8000/api/episodes/text" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "李四是一名产品经理，在上海的互联网公司工作",
    "description": "员工信息",
    "name": "李四档案",
    "reference_time": "20240104"
  }'

# 最简参数
curl -X POST "http://localhost:8000/api/episodes/text" \
  -H "Content-Type: application/json" \
  -d '{"content": "王五是一名后端工程师"}'

# 年月格式（自动补全为01日）
curl -X POST "http://localhost:8000/api/episodes/text" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "赵六是一名UI设计师",
    "reference_time": "202401"
  }'
```

## 🔧 时间格式说明

- **yyyyMMdd** (如: 20240104) → 直接使用指定日期
- **yyyyMM** (如: 202401) → 自动补全为20240101
- **留空** → 使用当前时间

## 📊 测试验证

运行测试脚本验证API功能：
```bash
uv run python test_api.py
```

测试内容包括：
- ✅ 健康检查端点
- ✅ API文档可访问性
- ✅ 完整参数请求
- ✅ 最简参数请求
- ✅ 年月格式时间处理
- ✅ 长文本内容处理

## 🎯 核心特性

1. **异步处理**: 基于FastAPI的异步架构，性能优秀
2. **数据验证**: Pydantic自动验证请求参数
3. **时间智能**: 支持多种时间格式，自动补全
4. **错误处理**: 完善的异常捕获和错误响应
5. **服务复用**: 智能的依赖注入管理
6. **标准兼容**: 遵循RESTful API设计规范

## ⚠️ 注意事项

1. **首次启动**: 服务启动时会初始化Neo4j连接和Graphiti，可能需要几秒时间
2. **LLM处理**: 文本情节添加涉及LLM处理，响应时间取决于文本长度
3. **时间格式**: 建议使用标准格式，避免歧义
4. **内容长度**: 支持长文本，但处理时间会相应增加

## 🔍 调试信息

查看服务日志可以获取详细的处理信息：
- Neo4j连接状态
- LLM请求和响应
- 情节添加进度
- 性能耗时统计

服务已成功运行，可以开始处理文本情节添加请求！