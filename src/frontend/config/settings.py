"""
前端系统配置文件
管理前端系统的各种配置参数
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class FrontendConfig:
    """前端系统配置类"""
    
    # 基础配置
    DEBUG = os.environ.get('FRONTEND_DEBUG', 'false').lower() == 'true'
    
    # 国际化配置
    DEFAULT_LANGUAGE = os.environ.get('FRONTEND_LANGUAGE', 'zh-CN')
    SUPPORTED_LANGUAGES = ['zh-CN', 'en-US']
    
    # 主题配置
    DEFAULT_THEME = os.environ.get('FRONTEND_THEME', 'light')  # light, dark, auto
    AUTO_THEME = os.environ.get('FRONTEND_AUTO_THEME', 'true').lower() == 'true'
    
    # API配置
    API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', '30000'))  # 毫秒
    
    # UI配置
    PAGE_TITLE = os.environ.get('PAGE_TITLE', 'Graphiti 知识图谱管理系统')
    COMPANY_NAME = os.environ.get('COMPANY_NAME', '企业名称')
    PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Graphiti 知识图谱')
    
    # 文件上传配置
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', '10485760'))  # 10MB
    ALLOWED_FILE_TYPES = ['text/plain', 'text/markdown', 'text/csv']
    
    # 搜索配置
    DEFAULT_SEARCH_LIMIT = int(os.environ.get('DEFAULT_SEARCH_LIMIT', '10'))
    MAX_SEARCH_LIMIT = int(os.environ.get('MAX_SEARCH_LIMIT', '50'))
    
    # 加载状态配置
    LOADING_TIMEOUT = int(os.environ.get('LOADING_TIMEOUT', '30000'))  # 毫秒
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """获取API配置"""
        return {
            'base_url': cls.API_BASE_URL,
            'timeout': cls.API_TIMEOUT,
            'endpoints': {
                'health': '/health',
                'add_text': '/api/episodes/text',
                'search': '/api/episodes/search'
            }
        }
    
    @classmethod
    def get_ui_config(cls) -> Dict[str, Any]:
        """获取UI配置"""
        return {
            'page_title': cls.PAGE_TITLE,
            'company_name': cls.COMPANY_NAME,
            'project_name': cls.PROJECT_NAME,
            'default_language': cls.DEFAULT_LANGUAGE,
            'supported_languages': cls.SUPPORTED_LANGUAGES,
            'default_theme': cls.DEFAULT_THEME,
            'auto_theme': cls.AUTO_THEME
        }
    
    @classmethod
    def get_file_config(cls) -> Dict[str, Any]:
        """获取文件上传配置"""
        return {
            'max_file_size': cls.MAX_FILE_SIZE,
            'allowed_file_types': cls.ALLOWED_FILE_TYPES
        }
    
    @classmethod
    def get_search_config(cls) -> Dict[str, Any]:
        """获取搜索配置"""
        return {
            'default_limit': cls.DEFAULT_SEARCH_LIMIT,
            'max_limit': cls.MAX_SEARCH_LIMIT
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置"""
        if cls.DEFAULT_LANGUAGE not in cls.SUPPORTED_LANGUAGES:
            raise ValueError(f"不支持的语言: {cls.DEFAULT_LANGUAGE}")
        
        if cls.DEFAULT_THEME not in ['light', 'dark', 'auto']:
            raise ValueError(f"不支持的主题: {cls.DEFAULT_THEME}")
        
        if cls.API_TIMEOUT <= 0:
            raise ValueError("API超时时间必须大于0")
        
        return True


# 默认配置实例
frontend_config = FrontendConfig()