"""
API请求数据模型
"""
from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class TextEpisodeRequest(BaseModel):
    """文本情节添加请求模型"""
    content: str = Field(..., description="长文本内容", min_length=1)
    description: Optional[str] = Field(default="文本信息", description="描述信息")
    name: Optional[str] = Field(default=None, description="情节名称，不传则自动生成")
    reference_time: Optional[str] = Field(default=None, description="参考时间，格式：yyyyMMdd或yyyyMM")
    
    @validator('reference_time')
    def validate_reference_time(cls, v):
        """验证reference_time格式"""
        if v is None:
            return v
        
        # 检查格式：yyyyMMdd (8位) 或 yyyyMM (6位)
        if len(v) == 8 and v.isdigit():
            # yyyyMMdd格式
            try:
                datetime.strptime(v, '%Y%m%d')
                return v
            except ValueError:
                return None  # 无效格式，后续会使用当前时间
        elif len(v) == 6 and v.isdigit():
            # yyyyMM格式，补全为01日
            try:
                datetime.strptime(v + '01', '%Y%m%d')
                return v + '01'
            except ValueError:
                return None  # 无效格式，后续会使用当前时间
        else:
            return None  # 无效格式，后续会使用当前时间
    
    class Config:
        schema_extra = {
            "example": {
                "content": "张三是一名软件工程师，在北京科技公司工作，主要负责前端开发。",
                "description": "员工信息",
                "name": "张三档案",
                "reference_time": "20240104"
            }
        }


class SearchRequest(BaseModel):
    """搜索请求模型"""
    query: str = Field(..., description="搜索查询词", min_length=1)
    limit: Optional[int] = Field(default=10, description="返回结果数量限制", ge=1, le=50)
    
    class Config:
        schema_extra = {
            "example": {
                "query": "软件工程师",
                "limit": 10
            }
        }