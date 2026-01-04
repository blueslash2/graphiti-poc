"""
API依赖注入管理
"""
from typing import AsyncGenerator
from contextlib import asynccontextmanager
import logging
from neo4j_connector import Neo4jConnector
from llm_graphiti_manager import LLMGraphitiManager
from knowledge_graph_builder import KnowledgeGraphBuilder
from config import config


class GraphService:
    """图谱服务类，封装知识图谱操作"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.neo4j_connector = None
        self.graphiti_manager = None
        self.graph_builder = None
        self._initialized = False
    
    async def initialize(self):
        """初始化服务"""
        if self._initialized:
            return
        
        try:
            self.logger.info("初始化图谱服务...")
            
            # 初始化Neo4j连接
            neo4j_config = config.get_neo4j_config()
            self.neo4j_connector = Neo4jConnector(
                uri=neo4j_config['uri'],
                user=neo4j_config['user'],
                password=neo4j_config['password']
            )
            self.neo4j_connector.validate_connection()
            
            # 初始化LLM和Graphiti管理器
            self.graphiti_manager = LLMGraphitiManager(self.neo4j_connector)
            await self.graphiti_manager.initialize_graphiti()
            await self.graphiti_manager.setup_database()
            
            # 初始化知识图谱构建器
            self.graph_builder = KnowledgeGraphBuilder(self.graphiti_manager)
            
            self._initialized = True
            self.logger.info("图谱服务初始化完成")
            
        except Exception as e:
            self.logger.error(f"图谱服务初始化失败: {e}")
            raise
    
    async def cleanup(self):
        """清理资源"""
        try:
            self.logger.info("清理图谱服务资源...")
            if self.graphiti_manager:
                await self.graphiti_manager.close_connection()
            self._initialized = False
            self.logger.info("图谱服务资源清理完成")
        except Exception as e:
            self.logger.error(f"清理图谱服务资源时出错: {e}")
    
    def get_graph_builder(self) -> KnowledgeGraphBuilder:
        """获取图谱构建器"""
        if not self._initialized:
            raise RuntimeError("服务未初始化")
        return self.graph_builder
    
    async def add_text_episode(self, content: str, description: str = "文本信息",
                             name: str = None, reference_time: str = None) -> dict:
        """添加文本情节"""
        try:
            from graphiti_core.nodes import EpisodeType
            from datetime import datetime, timezone
            
            # 处理参考时间
            ref_datetime = None
            if reference_time:
                try:
                    ref_datetime = datetime.strptime(reference_time, '%Y%m%d').replace(tzinfo=timezone.utc)
                except ValueError:
                    ref_datetime = datetime.now(timezone.utc)
            else:
                ref_datetime = datetime.now(timezone.utc)
            
            # 调用图谱构建器添加情节
            await self.graph_builder.add_single_episode(
                content=content,
                episode_type=EpisodeType.text,
                description=description,
                name=name
            )
            
            # 返回结果信息
            return {
                "name": name or f"情节_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": description,
                "content_preview": content[:50] + "..." if len(content) > 50 else content,
                "reference_time": reference_time or datetime.now().strftime('%Y%m%d'),
                "episode_type": "text"
            }
            
        except Exception as e:
            self.logger.error(f"添加文本情节失败: {e}")
            raise
    
    async def search_entities(self, query: str, limit: int = 10) -> dict:
        """搜索实体"""
        try:
            from knowledge_graph_searcher import KnowledgeGraphSearcher
            
            # 创建搜索器
            searcher = KnowledgeGraphSearcher(self.graphiti_manager)
            
            # 执行基本搜索
            search_results = await searcher.basic_search(query)
            
            # 转换结果为API格式
            results = []
            for result in search_results[:limit]:
                # 提取实体信息
                entity_data = {
                    "name": getattr(result, 'name', 'Unknown'),
                    "summary": getattr(result, 'summary', None),
                    "entity_type": getattr(result, 'entity_type', None),
                    "relevance_score": getattr(result, 'score', None),
                    "properties": {}
                }
                
                # 添加额外属性
                if hasattr(result, 'attributes'):
                    entity_data["properties"] = result.attributes
                elif hasattr(result, 'properties'):
                    entity_data["properties"] = result.properties
                
                results.append(entity_data)
            
            return {
                "query": query,
                "results": results,
                "total_count": len(search_results)
            }
            
        except Exception as e:
            self.logger.error(f"搜索实体失败: {e}")
            raise


# 全局服务实例
_graph_service = GraphService()


async def get_graph_service() -> GraphService:
    """获取图谱服务实例的依赖注入"""
    try:
        await _graph_service.initialize()
        return _graph_service
    except Exception as e:
        logger.error(f"获取图谱服务失败: {e}")
        raise


def get_graph_service_sync() -> GraphService:
    """同步获取图谱服务实例（用于非异步上下文）"""
    return _graph_service