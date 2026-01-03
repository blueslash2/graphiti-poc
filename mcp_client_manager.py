#!/usr/bin/env python3
"""
mcp_client_manager.py
最简 MCP 客户端封装，仅保留必要接口
"""
import asyncio
import logging
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager

# 定义日志前缀，明显标识来源
LOG_PREFIX = "[MCP_CLIENT]"

DEFAULT_SERVER_HTTP = "http://172.16.11.152:8000/mcp"


class MCPSessionManager:
    """最简 MCP 客户端管理器"""
    
    _instance: Optional['MCPSessionManager'] = None
    _lock = asyncio.Lock()
    def __init__(self):
        # 在现有属性基础上添加
        self._session_context = None
        self._client_context = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._instance._session = None
            cls._instance._client = None
            # 添加日志记录器
            cls._instance.logger = logging.getLogger(__name__ + ".MCPSessionManager")
        return cls._instance
    
    async def initialize(self, server_url: str = DEFAULT_SERVER_HTTP):
        """初始化连接（整个程序只需调用一次）"""
        self.logger.info(f"{LOG_PREFIX} 开始初始化MCP连接...")
        if not self._initialized:
            self.logger.info(f"{LOG_PREFIX} MCP未初始化，准备初始化...")
            async with self._lock:
                self.logger.info(f"{LOG_PREFIX} 获取到初始化锁...")
                if not self._initialized:
                    try:
                        self.logger.info(f"{LOG_PREFIX} 子步骤1: 使用上下文管理器建立完整连接...")
                        self.logger.info(f"{LOG_PREFIX} 服务器地址: {server_url}")

                        # 采用官方推荐的上下文管理器模式
                        async with streamable_http_client(url=server_url) as (read, write, get_sid):
                            self.read = read
                            self.write = write
                            self.get_sid = get_sid
                            self.logger.info(f"{LOG_PREFIX} HTTP客户端连接建立完成")
                            self.logger.info(f"{LOG_PREFIX} 会话ID: {get_sid() if get_sid else 'None'}")

                            # 创建并管理MCP会话
                            self.logger.info(f"{LOG_PREFIX} 子步骤2: 创建MCP会话...")
                            async with ClientSession(self.read, self.write) as session:
                                self._session = session

                                self.logger.info(f"{LOG_PREFIX} 子步骤3: 初始化MCP会话...")
                                await self._session.initialize()
                                self.logger.info(f"{LOG_PREFIX} MCP会话初始化完成")

                                self.logger.info(f"{LOG_PREFIX} 子步骤4: 获取可用工具列表...")
                                self._tools = await self._session.list_tools()
                                self.logger.info(f"{LOG_PREFIX} MCP连接成功，可用工具数量: {len(self._tools)}，工具列表: {[t.name for t in self._tools]}")

                                # 保存会话和连接信息
                                self._initialized = True
                                self._server_url = server_url
                                self.logger.info(f"{LOG_PREFIX} MCP初始化全部完成")

                                # 注意：由于上下文管理器会在退出时自动关闭连接，
                                # 我们需要保存会话状态，这里需要特殊处理
                                self._session_context = session  # 保存会话上下文
                                self._client_context = (read, write, get_sid)  # 保存客户端上下文

                    except Exception as e:
                        self.logger.error(f"{LOG_PREFIX} MCP初始化失败: {e}")
                        self.logger.error(f"{LOG_PREFIX} 失败详情 - 服务器地址: {server_url}")
                        # 清理已创建的资源
                        await self._cleanup_partial()
                        raise
        else:
            self.logger.info(f"{LOG_PREFIX} MCP已经初始化，跳过初始化步骤")


    
    async def add_episode(
        self,
        name: str,
        episode_body: str,
        source: str = "text",
        source_description: str = "",
    ) -> Dict[str, Any]:
        """调用远端 add_episode 工具"""
        self.logger.info(f"{LOG_PREFIX} 开始添加情节: {name}")
        self.logger.info(f"{LOG_PREFIX} 情节内容长度: {len(episode_body)} 字符")
        self.logger.info(f"{LOG_PREFIX} 情节来源: {source}")
        self.logger.info(f"{LOG_PREFIX} 情节描述: {source_description}")

        try:
            result = await self._call_tool(
                "add_episode",
                arguments={
                    "name": name,
                    "episode_body": episode_body,
                    "source": source,
                    "source_description": source_description,
                },
            )
            self.logger.info(f"{LOG_PREFIX} 情节添加成功: {name}")
            self.logger.debug(f"{LOG_PREFIX} 返回结果: {result}")
            return result
        except Exception as e:
            self.logger.error(f"{LOG_PREFIX} 情节添加失败: {name}")
            self.logger.error(f"{LOG_PREFIX} 错误信息: {e}")
            raise

#    async def get_episode(self, episode_id: str) -> Dict[str, Any]:
        #"""获取剧集（另一个业务方法）"""
        #return await self._call_tool("get_episode", {
            #"episode_id": episode_id
        #})
    
    # 你可以添加任意多的业务方法...
    
    async def _call_tool(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """内部工具调用方法（带错误处理）"""
        self.logger.info(f"{LOG_PREFIX} 准备调用工具: {tool_name}")
        self.logger.debug(f"{LOG_PREFIX} 工具参数: {arguments}")

        if not self._initialized or not self._session:
            self.logger.error(f"{LOG_PREFIX} 工具调用失败: MCP未初始化")
            raise RuntimeError("MCP未初始化，请先调用initialize()")

        try:
            self.logger.info(f"{LOG_PREFIX} 正在调用工具 {tool_name}...")
            result = await self._session.call_tool(tool_name, arguments=arguments)
            self.logger.info(f"{LOG_PREFIX} 工具调用成功: {tool_name}")
            self.logger.debug(f"{LOG_PREFIX} 工具返回结果: {result}")
            return result
        except Exception as e:
            self.logger.error(f"{LOG_PREFIX} 工具调用失败: {tool_name}")
            self.logger.error(f"{LOG_PREFIX} 错误详情: {e}")
            self.logger.error(f"{LOG_PREFIX} 失败参数: {arguments}")
            raise

    async def _cleanup_partial(self):
        """清理部分创建的资源"""
        try:
            if self._session:
                await self._session.aclose()
                self._session = None
            if self._client:
                await self._client.__aexit__(None, None, None)
                self._client = None
        except Exception as e:
            self.logger.warning(f"{LOG_PREFIX} 清理资源时出错: {e}")

    async def close(self):
        """关闭连接（程序退出时调用）"""
        self.logger.info(f"{LOG_PREFIX} 开始关闭MCP连接...")
        if self._initialized:
            try:
                # 由于使用了上下文管理器，这里主要是状态清理
                self._initialized = False
                self._session = None
                self._client = None
                self._session_context = None
                self._client_context = None
                self.logger.info(f"{LOG_PREFIX} MCP连接已完全关闭")
            except Exception as e:
                self.logger.error(f"{LOG_PREFIX} 关闭MCP连接时出错: {e}")
                raise
        else:
            self.logger.info(f"{LOG_PREFIX} MCP连接未初始化，无需关闭")


_mcp_manager_instance: Optional[MCPSessionManager] = None

async def get_mcp_manager(server_url: str = DEFAULT_SERVER_HTTP) -> MCPSessionManager:
    """
    获取全局唯一的MCP管理器实例
    
    Args:
        server_url: 可选，指定服务器地址，默认使用常量配置
    
    使用示例:
        # 不传入参数，使用默认配置
        manager = get_mcp_manager()
        await manager.initialize()
        
        # 或者传入自定义地址
        manager = get_mcp_manager("http://custom-server/mcp")
        await manager.initialize()
    """
    global _mcp_manager_instance
    # 添加函数级日志记录器
    func_logger = logging.getLogger(__name__ + ".get_mcp_manager")
    
    func_logger.info(f"{LOG_PREFIX} 开始获取MCP管理器实例...")
    func_logger.info(f"{LOG_PREFIX} 服务器地址: {server_url}")
    
    if _mcp_manager_instance is None:
        func_logger.info(f"{LOG_PREFIX} MCP管理器实例不存在，创建新实例...")
        _mcp_manager_instance = MCPSessionManager()
        func_logger.info(f"{LOG_PREFIX} MCP管理器实例创建完成")
    else:
        func_logger.info(f"{LOG_PREFIX} MCP管理器实例已存在，返回现有实例")
        func_logger.info(f"{LOG_PREFIX} 实例初始化状态: {'已初始化' if _mcp_manager_instance._initialized else '未初始化'}")
    
    return _mcp_manager_instance
