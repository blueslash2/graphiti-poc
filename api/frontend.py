"""
前端路由模块
处理前端页面的模板渲染和静态文件服务
"""
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional
import os
from datetime import datetime

from src.frontend.config.settings import frontend_config

# 创建路由实例
router = APIRouter(prefix="", tags=["前端页面"])

# 配置模板
templates = Jinja2Templates(directory="src/frontend/templates")

# 添加自定义过滤器
def format_datetime(value: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间"""
    if isinstance(value, datetime):
        return value.strftime(format)
    return str(value)

def to_json(value: Any) -> str:
    """转换为JSON字符串"""
    import json
    return json.dumps(value, ensure_ascii=False, default=str)

def get_entity_type_name(entity_type: str) -> str:
    """获取实体类型的显示名称"""
    type_names = {
        "PERSON": "人员",
        "COMPANY": "公司", 
        "ORGANIZATION": "组织",
        "POSITION": "职位",
        "SKILL": "技能",
        "PROJECT": "项目",
        "PRODUCT": "产品",
        "LOCATION": "地点",
        "EVENT": "事件",
        "WORKS_AS": "职位关系",
        "HAS_ROLE": "角色关系",
        "SPECIALIZES_IN": "专业关系",
        "RESPONSIBLE_FOR": "责任关系",
        "WORKS_AT": "工作地点关系"
    }
    return type_names.get(entity_type, entity_type)

# 注册过滤器
templates.env.filters["datetime"] = format_datetime
templates.env.filters["tojson"] = to_json
templates.env.filters["entity_type_name"] = get_entity_type_name

async def get_template_context(request: Request, page_title: str = "", active_page: str = "") -> Dict[str, Any]:
    """获取模板上下文"""
    return {
        "request": request,
        "page_title": page_title or frontend_config.PAGE_TITLE,
        "active_page": active_page,
        "company_name": frontend_config.COMPANY_NAME,
        "project_name": frontend_config.PROJECT_NAME,
        "version": "1.0.0",
        "build_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": frontend_config.DEFAULT_LANGUAGE,
        "theme": frontend_config.DEFAULT_THEME,
        "auto_theme": frontend_config.AUTO_THEME,
        "api_base_url": frontend_config.API_BASE_URL,
        "api_timeout": frontend_config.API_TIMEOUT,
        "max_file_size": frontend_config.MAX_FILE_SIZE,
        "frontend_config": {
            "language": frontend_config.DEFAULT_LANGUAGE,
            "theme": frontend_config.DEFAULT_THEME,
            "auto_theme": frontend_config.AUTO_THEME,
            "api_base_url": frontend_config.API_BASE_URL,
            "api_timeout": frontend_config.API_TIMEOUT,
            "max_file_size": frontend_config.MAX_FILE_SIZE,
            "company_name": frontend_config.COMPANY_NAME,
            "project_name": frontend_config.PROJECT_NAME,
            "version": "1.0.0"
        }
    }

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """首页面板"""
    context = await get_template_context(
        request, 
        page_title="首页面板 - Graphiti 知识图谱管理系统",
        active_page="dashboard"
    )
    return templates.TemplateResponse("pages/dashboard.html", context)

@router.get("/add-knowledge", response_class=HTMLResponse)
async def add_knowledge(request: Request):
    """新增知识页面"""
    context = await get_template_context(
        request,
        page_title="新增知识 - Graphiti 知识图谱管理系统", 
        active_page="add-knowledge"
    )
    return templates.TemplateResponse("pages/add-knowledge.html", context)

@router.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    """知识查询页面"""
    context = await get_template_context(
        request,
        page_title="知识查询 - Graphiti 知识图谱管理系统",
        active_page="search"
    )
    return templates.TemplateResponse("pages/search.html", context)

@router.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    """系统设置页面"""
    context = await get_template_context(
        request,
        page_title="系统设置 - Graphiti 知识图谱管理系统",
        active_page="settings"
    )
    return templates.TemplateResponse("pages/settings.html", context)

@router.get("/help", response_class=HTMLResponse)
async def help(request: Request):
    """帮助文档页面"""
    context = await get_template_context(
        request,
        page_title="帮助文档 - Graphiti 知识图谱管理系统",
        active_page="help"
    )
    return templates.TemplateResponse("pages/help.html", context)

@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    """隐私政策页面"""
    context = await get_template_context(
        request,
        page_title="隐私政策 - Graphiti 知识图谱管理系统"
    )
    return templates.TemplateResponse("pages/privacy.html", context)

@router.get("/terms", response_class=HTMLResponse)
async def terms(request: Request):
    """使用条款页面"""
    context = await get_template_context(
        request,
        page_title="使用条款 - Graphiti 知识图谱管理系统"
    )
    return templates.TemplateResponse("pages/terms.html", context)

@router.get("/404", response_class=HTMLResponse)
async def not_found(request: Request):
    """404错误页面"""
    context = await get_template_context(
        request,
        page_title="页面未找到 - Graphiti 知识图谱管理系统"
    )
    return templates.TemplateResponse("errors/404.html", context)

@router.get("/500", response_class=HTMLResponse)
async def server_error(request: Request):
    """500错误页面"""
    context = await get_template_context(
        request,
        page_title="服务器错误 - Graphiti 知识图谱管理系统"
    )
    return templates.TemplateResponse("errors/500.html", context)