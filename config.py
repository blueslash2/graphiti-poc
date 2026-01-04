"""
配置文件
管理应用程序的各种配置参数
"""
import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """应用程序配置类"""
    # Neo4j数据库配置
    NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://172.16.11.152:7687')
    NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'password')
    # LLM配置
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', 'http://192.168.200.2/v1')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'sk-RJ9cPqQnJ3fRUBgkuLoojfjhVTotPFqOo13IwCN3tD5Wxgh7')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', '衡云·明理')
    OPENAI_SMALL_MODEL = os.environ.get('OPENAI_SMALL_MODEL', '衡云·明理')
    OPENAI_EMBEDDING_MODEL = os.environ.get('OPENAI_EMBEDDING_MODEL', 'bge-m3')
    OPENAI_EMBEDDING_DIM = int(os.environ.get('OPENAI_EMBEDDING_DIM', '1024'))
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    @classmethod
    def get_neo4j_config(cls) -> dict:
        """获取Neo4j连接配置"""
        return {
            'uri': cls.NEO4J_URI,
            'user': cls.NEO4J_USER,
            'password': cls.NEO4J_PASSWORD
        }

    @classmethod
    def get_llm_config(cls) -> dict:
        """获取LLM配置"""
        return {
            'base_url': cls.OPENAI_BASE_URL,
            'api_key': cls.OPENAI_API_KEY,
            'model': cls.OPENAI_MODEL,
            'small_model': cls.OPENAI_SMALL_MODEL,
            'embedding_model': cls.OPENAI_EMBEDDING_MODEL,
            'embedding_dim': cls.OPENAI_EMBEDDING_DIM
        }

    @classmethod
    def validate_config(cls) -> bool:
        """验证配置"""
        required_configs = [
            cls.NEO4J_URI,
            cls.NEO4J_USER,
            cls.NEO4J_PASSWORD
        ]
        if not all(required_configs):
            raise ValueError(
                "配置不完整。请检查以下配置：\n"
                f"NEO4J_URI: {cls.NEO4J_URI}\n"
                f"NEO4J_USER: {cls.NEO4J_USER}\n"
                f"NEO4J_PASSWORD: {'已设置' if cls.NEO4J_PASSWORD else '未设置'}"
            )
        return True

# 默认配置实例
config = Config()
