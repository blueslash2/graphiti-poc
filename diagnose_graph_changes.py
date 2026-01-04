#!/usr/bin/env python3
"""
图数据库变化诊断脚本
用于分析添加数据前后图数据库的变化
"""
import asyncio
import logging
import time
from neo4j_connector import Neo4jConnector
from llm_graphiti_manager import LLMGraphitiManager
from knowledge_graph_builder import KnowledgeGraphBuilder
from knowledge_graph_searcher import KnowledgeGraphSearcher

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphChangeDiagnostic:
    """图数据库变化诊断器"""
    def __init__(self):
        self.neo4j_connector = None
        self.graphiti_manager = None
        self.graph_builder = None
        self.searcher = None

    async def initialize(self):
        """初始化"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("初始化诊断器...")
        try:
            # 初始化Neo4j连接
            self.neo4j_connector = Neo4jConnector()
            self.neo4j_connector.validate_connection()
            # 初始化Ollama和Graphiti管理器
            self.graphiti_manager = LLMGraphitiManager(self.neo4j_connector)
            await self.graphiti_manager.initialize_graphiti()
            await self.graphiti_manager.setup_database()
            # 初始化知识图谱构建器和搜索器
            self.graph_builder = KnowledgeGraphBuilder(self.graphiti_manager)
            self.searcher = KnowledgeGraphSearcher(self.graphiti_manager)
            self.logger.info("诊断器初始化完成")
        except Exception as e:
            self.logger.error(f"初始化失败: {e}")
            raise

    def get_detailed_graph_stats(self):
        """获取详细的图统计信息"""
        try:
            with self.neo4j_connector.driver.session() as session:
                # 基本统计
                result = session.run("MATCH (n) RETURN count(n) as node_count")
                node_count = result.single()["node_count"]
                result = session.run("MATCH ()-[r]->() RETURN count(r) as rel_count")
                rel_count = result.single()["rel_count"]
                # 节点标签统计
                result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count")
                label_stats = [(record["labels"], record["count"]) for record in result]
                # 关系类型统计
                result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
                type_stats = [(record["type"], record["count"]) for record in result]
                # 节点属性统计
                result = session.run("MATCH (n) RETURN n.name, properties(n) as props LIMIT 10")
                node_props = [(record["n.name"], record["props"]) for record in result]
                # 关系属性统计
                result = session.run("MATCH ()-[r]->() RETURN type(r), properties(r) as props LIMIT 10")
                rel_props = [(record["type(r)"], record["props"]) for record in result]
                return {
                    'node_count': node_count,
                    'rel_count': rel_count,
                    'label_stats': label_stats,
                    'type_stats': type_stats,
                    'node_props': node_props,
                    'rel_props': rel_props
                }
        except Exception as e:
            self.logger.error(f"获取图统计时出错: {e}")
        return None

    def print_graph_stats(self, stats, title):
        """打印图统计信息"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        if not stats:
            print("无法获取统计信息")
            return
        print(f"节点数量: {stats['node_count']}")
        print(f"关系数量: {stats['rel_count']}")
        print(f"\n节点标签统计:")
        for labels, count in stats['label_stats']:
            print(f"  {labels}: {count}")
        print(f"\n关系类型统计:")
        for rel_type, count in stats['type_stats']:
            print(f"  {rel_type}: {count}")
        print(f"\n节点属性示例 (前10个):")
        for name, props in stats['node_props']:
            print(f"  {name}: {props}")
        print(f"\n关系属性示例 (前10个):")
        for rel_type, props in stats['rel_props']:
            print(f"  {rel_type}: {props}")
