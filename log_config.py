#!/usr/bin/env python3
"""
全面的日志配置解决方案
隐藏各种已知的警告和错误信息
"""
import logging

def setup_comprehensive_logging():
    """设置全面的日志配置"""
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # 获取根日志记录器并添加处理器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # 设置Graphiti核心库的日志级别
    graphiti_modules = [
        'graphiti_core.utils.maintenance.edge_operations',
        'graphiti_core.driver.neo4j_driver',
        'graphiti_core',
        'graphiti_core.llm_client',
        'graphiti_core.embedder',
        'graphiti_core.cross_encoder'
    ]
    for module in graphiti_modules:
        logger = logging.getLogger(module)
        logger.setLevel(logging.WARNING)
    # 设置特定模块为ERROR级别（隐藏WARNING）
    error_modules = [
        'graphiti_core.utils.maintenance.edge_operations',
        'graphiti_core.driver.neo4j_driver'
    ]
    for module in error_modules:
        logger = logging.getLogger(module)
        logger.setLevel(logging.ERROR)
    # 设置httpx的日志级别（减少HTTP请求日志）
    logging.getLogger('httpx').setLevel(logging.WARNING)
    print("全面日志配置已设置")

if __name__ == "__main__":
    setup_comprehensive_logging()
