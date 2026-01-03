import asyncio
from typing import Any, Dict, Optional, Union, List
from datetime import datetime
from enum import Enum
from langchain_mcp_adapters.client import MultiServerMCPClient

# 直接从你原来的位置导入
from graphiti_core.nodes import EpisodeType

# ---------- 配置 ----------
SERVERS = {
    "remote": {
        "url": "http://172.16.11.152:8000/mcp",
        "transport": "streamable_http",
    }
}

# ---------- 内部工厂 ----------
_client: MultiServerMCPClient | None = None

async def _get_client() -> MultiServerMCPClient:
    global _client
    if _client is None:
        _client = MultiServerMCPClient(SERVERS)
    return _client

# ---------- 工具调用门面 ----------
async def _call_tool(tool_name: str, arguments: Dict[str, Any]) -> Any:
    """每次调用都临时连接，用完即断"""
    client = await _get_client()
    tools = await client.get_tools()

    #print(f"\n{'='*60}")
    #print(f"MCP服务器可用工具列表 (共 {len(tools)} 个):")
    #print(f"{'='*60}")
    #for i, tool in enumerate(tools, 1):
    #    tool_name_str = getattr(tool, 'name', 'Unknown')
        #tool_desc = getattr(tool, 'description', '无描述')
    #    print(f"{i}. {tool_name_str}")
    print(f"{'='*60}")
    print(f"正在调用工具: {tool_name}")
    print(f"{'='*60}\n")

    tool = None
    for t in tools:
        if hasattr(t, 'name') and t.name == tool_name:
            tool = t
            break
    if tool is None:
        raise ValueError(f"工具 '{tool_name}' 未找到")

    return await tool.ainvoke(arguments)

# ---------- 对外接口 ----------
async def add_episode(
    *,
    name: str,
    episode_body: str,
    source: Union[str, EpisodeType],
    source_description: str,
    reference_time: Optional[datetime] = None,
) -> Any:
    """随处直接调用，签名与你的上游代码完全匹配"""
    source_str = source.value if isinstance(source, Enum) else str(source)
    
    args = {
        "name": name,
        "episode_body": episode_body,
        "source": source_str,
        "source_description": source_description,
    }
    if reference_time is not None:
        args["reference_time"] = reference_time.isoformat()
    
    return await _call_tool("add_memory", args)

# ---------- 搜索相关对外接口 ----------
async def search_nodes(
    *,
    query: str,
    max_nodes: int = 10,
    group_ids: Optional[List[str]] = None,
) -> Any:
    """搜索知识图谱中的节点"""
    args = {
        "query": query,
        "max_nodes": max_nodes,
    }
    if group_ids is not None:
        args["group_ids"] = group_ids
    
    return await _call_tool("search_nodes", args)

async def search_memory_facts(
    *,
    query: str,
    max_facts: int = 10,
    center_node_uuid: Optional[str] = None,
    group_ids: Optional[List[str]] = None,
) -> Any:
    """搜索知识图谱中的记忆事实"""
    args = {
        "query": query,
        "max_facts": max_facts,
    }
    if center_node_uuid is not None:
        args["center_node_uuid"] = center_node_uuid
    if group_ids is not None:
        args["group_ids"] = group_ids
    
    return await _call_tool("search_memory_facts", args)


# 重新导出，这样你的主类只需要从这一个地方导入
__all__ = ['add_episode', 'search_nodes', 'search_memory_facts', 'EpisodeType']