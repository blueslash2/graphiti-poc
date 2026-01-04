# Neo4j查询参考手册

这些查询**在远程服务端执行**，客户端通过API调用。

## 基础统计查询

### 获取节点和关系总数
```cypher
MATCH (n) RETURN count(n) as node_count
MATCH ()-[r]->() RETURN count(r) as edge_count
```

### 获取节点标签分布
```cypher
MATCH (n) 
RETURN labels(n) as labels, count(n) as count 
ORDER BY count DESC
```

### 获取关系类型分布
```cypher
MATCH ()-[r]->() 
RETURN type(r) as relation_type, count(r) as count 
ORDER BY count DESC
```

## Graphiti生成的图结构
Graphiti会自动创建以下标签节点：
- __Episode__: 情节节点（原始输入）
- __Entity__: 实体节点（如"张三"）
- __Relationship__: 关系边（如"工作于"）

### 查询所有员工实体
```cypher
MATCH (e:__Entity__)
WHERE e.name CONTAINS "工程师" OR e.name CONTAINS "经理"
RETURN e.name, e.uuid
LIMIT 20
```

### 查询某人的完整信息网络
```cypher
MATCH (person:__Entity__ {name: "张三"})
CALL apoc.path.expandConfig(person, {
  relationshipFilter: ">",
  labelFilter: ">",
  minLevel: 1,
  maxLevel: 3
})
YIELD path
RETURN path
```

### 查询最新更新的节点（按时间排序）
```cypher
MATCH (n)
WHERE n.created_at IS NOT NULL
RETURN n.name, n.created_at
ORDER BY n.created_at DESC
LIMIT 10
```

## 性能优化查询

### 添加索引（Graphiti的setup_database已自动执行）
```cypher
CREATE INDEX episode_uuid IF NOT EXISTS FOR (e:__Episode__) ON (e.uuid)
CREATE INDEX entity_name IF NOT EXISTS FOR (e:__Entity__) ON (e.name)
```

### 清理孤立节点
```cypher
MATCH (n) WHERE NOT (n)--() DELETE n
```

## 调试查询

### 查看Graphiti构建的边属性
```cypher
MATCH ()-[r]->() 
RETURN type(r), r.fact, r.valid_at, r.invalid_at 
LIMIT 10
```

### 统计某个Episode的影响范围
```cypher
MATCH (ep:__Episode__ {name: "张三信息更新"})
CALL apoc.path.spanningTree(ep, {
  relationshipFilter: ">",
  labelFilter: ">"
})
YIELD path
RETURN count(path) as affected_nodes
```

## 服务端使用说明
这些查询**不应在客户端直接执行**，而应通过Graphiti服务封装：
**客户端调用远程服务 → 服务端执行Cypher → 返回结构化结果**
如需扩展查询，请在服务端实现新API端点。
