# 源代码介绍

## 整体说明
写了一个工程用来模拟如何构建知识图谱、针对知识图谱进行各类查询、并评测基于已有知识图谱新增节点或者更新原有节点的相关信息。

参考官方的例子https://github.com/getzep/graphiti/tree/main/examples/quickstart 进行了改写。我主要的优化点如下：

把官方example的面向过程写法改为了面向对象写法, 便于基于SRP单一职责原则进行维护。
把官方example同步写法改造为异步写法，提升数十倍（实测9.6倍左右）构建和查询效率。
官方写法是需要用OPENAI_API_KEY的，将其改造为依托本地 Ollama的方式，减少cost消耗。

整个工程如下所示:
src/
├── config.py                   # 配置管理
├── graphiti_service_client.py # 远程服务客户端
├── knowledge_graph_builder.py  # 知识图谱构建器
└── knowledge_graph_searcher.py # 知识图谱查询器
main.py                         # 基础演示
main2.py                        # 增量更新演示
- 配置相关的py文件有config.py以及log_config.py
- 资源管理器相关的py文件有neo4j_connector.py以及ollama_graphiti_manager.py
- 与图谱相关的操作工具py文件有 knowledge_graph_builder.py,knowledge_graph_searcher.py以及diagnose_graph_change.py
- 测试用例相关的py文件有main.py以及main2.py

## 源代码分析

### 配置文件config.py

config.py主要是用来维护各种配置。比如Neo4j数据库的配置、Ollama配置、日志配置等。

### 日志配置文件log_config.py

这个文件主要用来设置全局日志级别，尤其是与graphiti相关的。主要为了在研究日志分析其能力的时候有所取舍和侧重点。

### neo4j连接器neo4j_connector.py

这个文件主要负责连接neo4j，它主要提供设置初始化连接(__init___、设置日志级别(_setup_logging)、加载环境变量(_load_environment)、连接参数校验(_validate_connection_params)、连接参数获取(get_connection_params)、连接参数更新(update_connection_params)等操作。另外，它提供了一个异步方法(clean_database)来清理数据库中的数据，方便反复实验。

### graphiti管理器 ollama_graphiti_manager.py

因为我从OPENAI切换为了本地ollama，所以这里起名为ollama_graphiti_manager.py。它主要的职责是，配置依托ollama的生成模型（setup_ollama_config）、配置依托ollama的嵌入模型（setup_embedder）、配置cross_encoder(setup_cross_encoder) 、异步的初始化graphiti实例（initialize_graphiti）、异步方法设置数据库并清理和构建索引（setup_database）、关闭连接（close_connection）等操作。

### kg关键能力-知识图谱构造器 knowledge_graph_builder.py

这个是知识图谱的关键能力，主要用于构造知识图谱。它主要包含以下能力：

1. [通用能力]创建情节数据，对应方法为create_episode_data方法, 它是被其他方法调用用来创建情节数据。
2. 创建文本情节数据create_text_episode方法。它主要用来创建episode_type=EpisodeType.text类型的情节数据，并且通过调用#1的create_episode_data(）方法来实现。
3. 创建json情节数据create_json_episode方法。它主要用来创建episode_type=EpisodeType.json的情节数据，并且通过调用#1的create_episode_data()方法来实现。
4. 转换json到文本 convert_json_to_text方法。它主要把JSON数据转化为自然语言文本。
5. 添加多个情节数据到知识图谱add_episodes。它主要把多个情节数据利用框架的graphiti.add_episode方法依次添加到知识图谱中。
6. 添加单个情节数据到知识图谱add_single_episode方法。它主要把单个情节数据添加到知识图谱。
7. 添加json的情节数据add_json_episode方法。它主要用来负责添加json类型的情节数据。
8. 批量创建情节数据create_episode_batch方法。它会遍历并批量调用#1的create_episode_data(）来批量调用情节数据。
9. 批量创建文本情节数据create_text_episode_batch方法。它会用来批量创建文本情节数据。它主要通过调用#8的create_episode_batch来实现。
10. 批量创建json情节数据 create_json_episode_batch方法。它会用来批量创建json情节数据。它主要通过调用#8的create_episode_batch来实现。

### kg关键能力-知识图谱查询器knowledge_graph_searcher.py

这个主要是知识图谱查询器，用于满足各种场景的基于知识图谱的查询。主要实现的功能有：

1. 基本搜索basic_search方法。它主要是基于query问题，基于知识图谱进行检索。主要是结合语义相似性和BM25文本检索。
2. 中心节点搜索center_node_search方法。它主要是基于图距离重新排序搜索结果。这个在知识图谱中用的很多，因为它会先锚定一个节点ID,然后看基于这个中心节点的搜索。
3. 搜索配方的搜索node_search_with_recipe方法。它主要是采用搜索配方的搜索，它直接检索节点而不是边。
4. 打印搜索结果print_search_results方法。它主要用来打印搜索结果，把搜索到的结果进行遍历。
5. 打印节点搜索结果print_node_search_results方法。它主要用来遍历并打印节点搜索结果。它主要用来打印和节点相关的信息，比如内容摘要、节点标签、创建时间等。
6. 带中心节点重排序的搜索search_with_center_node_reranking方法。它主要用来执行带中心节点的重排序的搜索，它先执行基本搜索，然后使用第一个节点作为中心节点来进行中心节点搜索。
7. 综合搜索comprehensive_search方法。它会执行所有的搜索。即先基本搜索，然后节点搜索，如果基本搜索有结果，再执行中心节点搜索。
8. 综合打印print_comprehensive_results方法。它会执行综合打印，也就是依次打印基本搜索结果、节点搜索结果和中心搜索结果。
9. 获得图谱的汇总数据get_graph_summary。它会进行知识图谱的汇总，它基于MATCH (n) RETURN count(n) as node_count获得节点数量，基于MATCH ()-[r]->() RETURN count(r) as edge_count获得边的数量，并且构造返回对象。

### kg关键能力-图数据库诊断器diagnose_graph_changes.py

1. 这个是图数据库诊断器，它主要用来获取作为知识图谱载体的图数据库的详细信息，比如：

- get_detailed_graph_stats方法是用来获得图数据库的详细统计信息，具体实现方式为：
- 利用MATCH (n) RETURN count(n) as node_count来获得图数据库节点数量
- 利用MATCH ()-[r]->() RETURN count(r) as rel_count来获得图数据库边的数量
- 利用MATCH (n) RETURN labels(n) as labels, count(n) as count来获得节点标签统计
- 利用MATCH ()-[r]->() RETURN type(r) as type, count(r) as count来获得关系类型统计
- 利用MATCH (n) RETURN n.name, properties(n) as props LIMIT 10来获得节点属性统计
- 利用MATCH ()-[r]->() RETURN type(r), properties(r) as props LIMIT 10来获得关系属性统计

### 测试用例main.py （演示知识图谱构建和查询）

main.py测试用例主要用来演示于知识图谱构建以及查询相关的效果。

1. build_knowledge_graph方法主要演示了如何构建知识图谱的过程。它先创建一组示例数据{张三、李四、王五、赵六}，有文本情节（text_episode）也有json情节（json_episode), 然后调用graph_builder.add_episodes方法来进行知识图谱构建。注意，技巧是通过await关键词进行跨协程交互。
2. perform_search方法主要演示了基于已经构建好的知识图谱执行基本搜索、节点搜索、中心节点搜索以及综合搜索的过程。比如基于工程师、软件工程师、技术总监等进行搜索。
3. add_custom_episodes 方法主要用来添加自定义情节。这里演示了添加2个episode{陈七，一个是孙八}。
4. 在run_demo方法中，依次会先构建知识图谱、再添加自定义情节，最后执行知识图谱搜索。

### 测试用例main2.py (主要用来观察添加新节点和边，以及合并到原有知识图谱)

这个测试用例主要是在原有的main.py构建出的知识图谱的基础上，做一些知识图谱更新的操作。

1. 新增节点（比如姓名为李九的员工，在新增了一个项目叫智能客服，并且其主要成员中包含李九和其他人），来利用get_graph_summary(）自定义方法来观察并打印知识图谱的变化。然后，依托新的知识图谱进行搜索，比如搜索姓名为“李九”的人，搜索名称为“智能客服”的项目，并观察耗时从而检验知识图谱性能。
2. 在原有某个节点比如张三上进行相关属性的修改（例如本例子中，把它的信息进行更新，从原来的软件工程师晋升为高级软件工程师，工作经验变长，技能标签变多，绩效变优），然后通过get_graph_summary()来观察并打印知识图谱的变化，这里期望是节点数量不变但是边的数量变化了，因为有了新的关系。并且针对更新的信息“张三”，在新的知识图谱上进行各个维度的搜索（比如按照薪资、绩效、技能等维度来搜索）。

## 快速开始
```bash
# 1. 配置
cp .env.example .env
# 编辑.env填写远程服务地址

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行演示
python main.py
```
## 远程服务要求（改造中）
- Graphiti服务需暴露REST API
- 支持 /health, /api/v1/episodes, /api/v1/search 端点
- 详见 CONFIGURATION.md