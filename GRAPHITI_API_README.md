# 参数对比：MCP add_memory vs graphiti_core add_episode

两者参数高度一致，但存在一些关键差异：

## 参数对比表
|Graphiti MCP服务器add_memory工具参数 | graphiti_core库add_episode方法参数 | 匹配度 | 说明
| name | name | 完全匹配 | episode 名称 |
| episode_body | episode_body | 完全匹配 | episode 内容 |
| group_id | group_id | 完全匹配 | 图分区标识 |
| source | source | 类型差异 | MCP 用 string，core 用 EpisodeType 枚举 |
| source_description | source_description | 完全匹配 | 源描述 |
| uuid | uuid | 完全匹配 | 可选 UUID |
| reference_time | × MCP 缺失 | 时间戳参数 |  |
| update_communities | × MCP 缺失 | 社区更新选项 |  |
| entity_types | × MCP 缺失 | 实体类型定义 |  |
| excluded_entity_types | × MCP 缺失 | 排除的实体类型 |  |
| previous_episode_uuids | × MCP 缺失 | 前置 episode UUID |  |
| edge_types | × MCP 缺失 | 边类型定义 |  |
| edge_type_map | × MCP 缺失 | 边类型映射 |  |

## 关键差异分析
1. 参数简化
MCP服务器的add_memory只暴露了最核心的6个参数，隐藏了高级配置选项 graphiti_mcp_server.py:321-367 。
2. source参数类型差异
MCP: 使用字符串（"text"、"json"、"message"） graphiti_mcp_server.py:377-385
Core: 使用EpisodeType枚举 graphiti.py:621
3. 缺失的高级参数
MCP接口省略了以下高级参数：
reference_time: 使用当前时间作为默认值
update_communities: 默认不更新社区
entity_types/excluded_entity_types: 使用服务器配置的实体类型
edge_types/edge_type_map: 使用默认边类型配置
previous_episode_uuids: 自动检索最近的episodes

## 本项目使用实例
在knowledge_graph_builder.py中add_episodes方法对情节List进行了处理：
await graphiti.add_episode(
    name=name,
    episode_body=episode_body,
    source=episode_type,
    source_description=description,
    reference_time=datetime.now(timezone.utc),
)

本项目调用本地库只使用了name, episode_body, source, source_description, reference_time五个参数，其中只有reference_time取的是系统当前时间，并且在MCP中不存在。
不过没关系，如果需要改造为调用MCP服务器，会自动使用当前时间作为reference_time，不需要传递此参数。

本项目没有使用group_id字段。group_id 最贴切的比喻是数据表或独立数据库。它是一个图分区标识符，用于在同一个图数据库中创建完全隔离的数据空间。如果是上市公司年报分析方案，每家公司使用一个group_id，在同一家公司的group_id下构建时序知识图谱。

### group_id技术实现细节
1. 数据隔离：所有操作都通过group_id过滤，确保不同公司的数据完全隔离
2. 时序查询：可以在同一group_id内按时间查询，追踪公司发展轨迹
3. 批量管理：支持按group_id批量删除数据，便于数据管理

### 使用建议
- 命名规范：建议使用股票代码或公司标识符（如aapl、msft、tsla）
- 查询优化：搜索时指定group_ids参数可提高查询效率
- 数据管理：可使用clear_graph工具清理特定公司的数据

### Notes
- group_id必须只包含字母数字、连字符或下划线
- MCP服务器支持默认group_id，但明确指定更利于数据管理
- 同一group_id内的episodes按顺序处理，保证时序数据的正确性