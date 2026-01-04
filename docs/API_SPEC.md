# Graphiti API Specification

## Service Info
- Base URL: `http://localhost:8000`
- Health Check: `GET /health`
- API Docs: `GET /docs` (Swagger), `GET /redoc` (ReDoc)

## Endpoints

### 1. Add Text Episode
**POST** `/api/episodes/text`

Request Body:
```json
{
  "content": "string, min_length=1, required",        // Long text content
  "description": "string, default='文本信息'",       // Episode description
  "name": "string, optional",                      // Episode name, auto-generated if null
  "reference_time": "string, optional"             // Time format: yyyyMMdd or yyyyMM
}
```

Response 200:
```json
{
  "success": true,
  "message": "string",
  "data": {
    "name": "string",                                // Episode name
    "description": "string",                         // Episode description
    "content_preview": "string",                     // First 50 chars + "..."
    "reference_time": "string|null",                 // Reference time
    "episode_type": "text"                           // Always "text"
  }
}
```

Response 400: Invalid request parameters
Response 500: Server error

Time format rules:
- yyyyMMdd (8 digits) → use as-is
- yyyyMM (6 digits) → append "01" → yyyyMM01
- Invalid/empty → use current time

### 2. Search Entities
**GET** `/api/episodes/search`

Query Parameters:
- `query`: string, required, min_length=1     // Search query
- `limit`: integer, optional, default=10, range=[1,50]  // Result limit

Response 200:
```json
{
  "success": true,
  "message": "string",
  "query": "string",                               // Original query
  "results": [
    {
      "name": "string",                             // Entity/relationship name
      "summary": "string|null",                     // Entity summary
      "entity_type": "string|null",                 // Entity type
      "relevance_score": "number|null",             // Similarity score [0.0, 1.0]
      "properties": {}                              // Additional properties
    }
  ],
  "total_count": "integer"                         // Total results found
}
```

Response 400: Invalid query parameters
Response 500: Server error

## Data Processing

### Text Processing Flow
```
text_input → LLM_analysis → entity_extraction → relationship_building → graph_storage → vector_indexing
```

### Search Mechanism
```
query → vector_embedding → similarity_matching → result_ranking → response
```

## Performance
- Text processing: 5-30s (depends on text complexity)
- Entity search: 0.3-1s (vector similarity computation)
- Concurrent requests: supported via async architecture

## Error Codes
- 400: Bad Request - invalid parameters
- 500: Internal Server Error - processing failure
- 200: Success

## Time Formats
reference_time parameter:
- Pattern: ^\d{6}$|^\d{8}$
- yyyyMMdd → direct parse
- yyyyMM → append "01"
- Invalid → current time UTC

## Vector Search
- Embedding model: configured via config.py
- Similarity metric: cosine similarity
- Index type: vector similarity search
- Relevance threshold: adaptive based on query

## Entity Types (from search results)
- WORKS_AS: job position relationships
- HAS_ROLE: role assignments
- SPECIALIZES_IN: skill specializations
- RESPONSIBLE_FOR: responsibility mappings
- WORKS_AT: company/location relationships

## Request Examples

Add episode:
```bash
curl -X POST "http://localhost:8000/api/episodes/text" \
  -H "Content-Type: application/json" \
  -d '{"content": "张三是一名软件工程师，在北京工作"}'
```

Search entities:
```bash
curl "http://localhost:8000/api/episodes/search?query=软件工程师&limit=5"
```

Health check:
```bash
curl "http://localhost:8000/health"
```

## Response Validation
- All responses include "success" boolean
- Error responses include "detail" field
- Data payloads wrapped in "data" object
- Consistent field naming across endpoints