"""
API响应数据模型
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class EpisodeResponseData(BaseModel):
    """情节响应数据"""
    name: str = Field(..., description="情节名称")
    description: str = Field(..., description="描述信息")
    content_preview: str = Field(..., description="内容预览（前50字符）")
    reference_time: Optional[str] = Field(None, description="参考时间")
    episode_type: str = Field(default="text", description="情节类型")


class EpisodeResponse(BaseModel):
    """情节添加响应模型"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    data: EpisodeResponseData = Field(..., description="响应数据")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "文本情节添加成功",
                "data": {
                    "name": "情节_20240104_120000",
                    "description": "员工信息",
                    "content_preview": "张三是一名软件工程师，在北京科技公司工作...",
                    "reference_time": "20240104",
                    "episode_type": "text"
                }
            }
        }


class SearchResultData(BaseModel):
    """搜索结果数据"""
    name: str = Field(..., description="实体名称")
    summary: Optional[str] = Field(None, description="实体摘要")
    entity_type: Optional[str] = Field(None, description="实体类型")
    relevance_score: Optional[float] = Field(None, description="相关性评分")
    properties: Dict[str, Any] = Field(default_factory=dict, description="实体属性")


class SearchResponse(BaseModel):
    """搜索响应模型"""
    success: bool = Field(..., description="操作是否成功")
    message: str = Field(..., description="响应消息")
    query: str = Field(..., description="搜索查询")
    results: List[SearchResultData] = Field(..., description="搜索结果列表")
    total_count: int = Field(..., description="结果总数")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "搜索成功",
                "query": "软件工程师",
                "results": [
                    {
                        "name": "张三",
                        "summary": "软件工程师，在北京科技公司工作",
                        "entity_type": "Person",
                        "relevance_score": 0.95,
                        "properties": {
                            "position": "软件工程师",
                            "location": "北京",
                            "company": "科技公司"
                        }
                    }
                ],
                "total_count": 1
            }
        }


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = Field(default=False, description="操作是否成功")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="详细错误信息")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "添加文本情节失败",
                "detail": "数据库连接错误"
            }
        }