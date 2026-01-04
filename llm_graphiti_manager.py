import logging
from typing import Optional
from graphiti_core import Graphiti
from graphiti_core.llm_client.config import LLMConfig
from graphiti_core.llm_client.openai_generic_client import OpenAIGenericClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.cross_encoder.openai_reranker_client import OpenAIRerankerClient
from config import config


class LLMGraphitiManager:
    """LLM连接和Graphiti初始化管理类"""
    def __init__(self, neo4j_connector):
        self.neo4j_connector = neo4j_connector
        self.graphiti: Optional[Graphiti] = None
        self.llm_client: Optional[OpenAIGenericClient] = None
        self.embedder: Optional[OpenAIEmbedder] = None
        self.cross_encoder: Optional[OpenAIRerankerClient] = None
        self.logger = logging.getLogger(__name__)

    def setup_llm_config(self):
        """配置LLM客户端"""
        self.logger.info("配置LLM客户端...")
        # 从配置文件获取LLM配置
        llm_config = config.get_llm_config()
        # 配置LLM客户端
        llm_config = LLMConfig(
            api_key=llm_config['api_key'],
            model=llm_config['model'],
            small_model=llm_config['small_model'],
            base_url=llm_config['base_url'],
        )
        self.llm_client = OpenAIGenericClient(config=llm_config)
        self.logger.info("LLM客户端配置完成")
        return llm_config

    def setup_embedder(self, llm_config):
        """配置Embedder"""
        self.logger.info("配置Embedder...")
        # 从配置文件获取llm配置
        llm_config = config.get_llm_config()
        self.embedder = OpenAIEmbedder(
            config=OpenAIEmbedderConfig(
                api_key=llm_config['api_key'],
                embedding_model=llm_config['embedding_model'],
                embedding_dim=llm_config['embedding_dim'], # bge-large-zh-v1.5是1024维
                base_url=llm_config['base_url'],
            )
        )
        self.logger.info("Embedder配置完成")
        return self.embedder

    def setup_cross_encoder(self, llm_client, llm_config):
        """配置Cross Encoder"""
        self.logger.info("配置Cross Encoder...")
        self.cross_encoder = OpenAIRerankerClient(client=llm_client, config=llm_config)
        self.logger.info("Cross Encoder配置完成")
        return self.cross_encoder

    async def initialize_graphiti(self):
        """初始化Graphiti实例"""
        self.logger.info("初始化Graphiti...")
        # 获取Neo4j连接参数
        conn_params = self.neo4j_connector.get_connection_params()
        # 设置LLM配置
        llm_config = self.setup_llm_config()
        embedder = self.setup_embedder(llm_config)
        cross_encoder = self.setup_cross_encoder(self.llm_client, llm_config)
        # 初始化Graphiti
        self.graphiti = Graphiti(
            conn_params['uri'],
            conn_params['user'],
            conn_params['password'],
            llm_client=self.llm_client,
            embedder=embedder,
            cross_encoder=cross_encoder,
        )
        self.logger.info("Graphiti初始化完成")
        return self.graphiti

    async def setup_database(self):
        """设置数据库（清理和构建索引）"""
        if not self.graphiti:
            raise ValueError("Graphiti未初始化")
        self.logger.info("设置数据库...")
        # 清理数据库
        await self.neo4j_connector.clean_database(self.graphiti.driver)
        # 初始化图数据库的Graphiti索引
        await self.graphiti.build_indices_and_constraints()
        self.logger.info("数据库设置完成")

    async def close_connection(self):
        """关闭连接"""
        if self.graphiti:
            await self.graphiti.close()
            self.logger.info("Graphiti连接已关闭")

    def get_graphiti(self) -> Graphiti:
        """获取Graphiti实例"""
        if not self.graphiti:
            raise ValueError("Graphiti未初始化")
        return self.graphiti
