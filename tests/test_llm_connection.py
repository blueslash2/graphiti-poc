#!/usr/bin/env python3
"""
测试LLM连接脚本
用于验证LLM配置是否正确
"""
import os
import sys
import asyncio
import logging
from config import config

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_llm_connection():
    """测试LLM连接"""
    try:
        logger.info("开始测试LLM连接...")
        
        # 获取LLM配置
        llm_config = config.get_llm_config()
        logger.info(f"LLM配置: {llm_config}")
        
        # 测试HTTP连接
        import httpx
        async with httpx.AsyncClient() as client:
            try:
                # 尝试访问base_url的根路径
                base_url_root = llm_config['base_url'].replace('/v1', '')
                response = await client.get(base_url_root, timeout=10.0)
                logger.info(f"HTTP根连接测试成功: {response.status_code}")
                
                # 尝试访问API端点
                api_url = llm_config['base_url'] + '/chat/completions'
                response = await client.post(
                    api_url,
                    json={
                        "model": llm_config['model'],
                        "messages": [{"role": "user", "content": "你好"}],
                        "max_tokens": 50
                    },
                    headers={"Authorization": f"Bearer {llm_config['api_key']}"},
                    timeout=10.0
                )
                logger.info(f"API端点测试成功: {response.status_code}")
                if response.status_code == 200:
                    logger.info(f"API响应: {response.text[:200]}...")
            except Exception as e:
                logger.error(f"HTTP连接测试失败: {e}")
        
        # 测试OpenAI API调用
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(
                api_key=llm_config['api_key'],
                base_url=llm_config['base_url']
            )
            
            logger.info("尝试调用API...")
            response = await client.chat.completions.create(
                model=llm_config['model'],
                messages=[{"role": "user", "content": "你好"}],
                max_tokens=50
            )
            
            logger.info(f"API调用成功: {response}")
            logger.info(f"响应内容: {response.choices[0].message.content}")
            
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            logger.error(f"错误类型: {type(e)}")
            
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
        logger.error(f"错误类型: {type(e)}")

if __name__ == "__main__":
    asyncio.run(test_llm_connection())