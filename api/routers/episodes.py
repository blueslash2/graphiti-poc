"""
情节管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any
import logging

from api.models.requests import TextEpisodeRequest, SearchRequest
from api.models.responses import EpisodeResponse, SearchResponse, ErrorResponse
from api.dependencies import get_graph_service, GraphService


router = APIRouter(prefix="/api/episodes", tags=["情节管理"])
logger = logging.getLogger(__name__)


@router.post("/text", response_model=EpisodeResponse, responses={
    400: {"model": ErrorResponse, "description": "请求参数错误"},
    500: {"model": ErrorResponse, "description": "服务器内部错误"}
})
async def add_text_episode(
    request: TextEpisodeRequest,
    graph_service: GraphService = Depends(get_graph_service)
) -> EpisodeResponse:
    """
    添加文本情节
    
    将长文本内容添加为知识图谱中的情节节点。
    """
    try:
        logger.info(f"收到添加文本情节请求: {request.name or '自动生成'}")
        
        # 调用服务添加文本情节
        result = await graph_service.add_text_episode(
            content=request.content,
            description=request.description,
            name=request.name,
            reference_time=request.reference_time
        )
        
        logger.info(f"文本情节添加成功: {result['name']}")
        
        return EpisodeResponse(
            success=True,
            message="文本情节添加成功",
            data=result
        )
        
    except ValueError as e:
        logger.error(f"请求参数错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "请求参数错误",
                "detail": str(e)
            }
        )
        
    except Exception as e:
        logger.error(f"添加文本情节失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "添加文本情节失败",
                "detail": str(e)
            }
        )


@router.get("/search", response_model=SearchResponse, responses={
    400: {"model": ErrorResponse, "description": "请求参数错误"},
    500: {"model": ErrorResponse, "description": "服务器内部错误"}
})
async def search_entities(
    query: str = Query(..., description="搜索查询词", min_length=1),
    limit: int = Query(10, description="返回结果数量限制", ge=1, le=50),
    graph_service: GraphService = Depends(get_graph_service)
) -> SearchResponse:
    """
    搜索实体
    
    在知识图谱中搜索相关实体和关系。
    """
    try:
        logger.info(f"收到搜索请求: {query}")
        
        # 调用服务搜索实体
        search_result = await graph_service.search_entities(query, limit)
        
        logger.info(f"搜索完成，找到 {search_result['total_count']} 个结果")
        
        return SearchResponse(
            success=True,
            message="搜索成功",
            query=query,
            results=search_result["results"],
            total_count=search_result["total_count"]
        )
        
    except ValueError as e:
        logger.error(f"搜索参数错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": "搜索参数错误",
                "detail": str(e)
            }
        )
        
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": "搜索失败",
                "detail": str(e)
            }
        )


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "episodes",
        "timestamp": ""
    }