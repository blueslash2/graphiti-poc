"""
FastAPI主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
from typing import Dict, Any

from api.routers import episodes
from api.dependencies import get_graph_service_sync


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Graphiti知识图谱API",
    description="基于Graphiti的知识图谱管理API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该配置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("正在启动Graphiti知识图谱API...")
    try:
        # 初始化图谱服务
        graph_service = get_graph_service_sync()
        await graph_service.initialize()
        logger.info("Graphiti知识图谱API启动完成")
    except Exception as e:
        logger.error(f"API启动失败: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("正在关闭Graphiti知识图谱API...")
    try:
        # 清理资源
        graph_service = get_graph_service_sync()
        await graph_service.cleanup()
        logger.info("Graphiti知识图谱API关闭完成")
    except Exception as e:
        logger.error(f"API关闭时出错: {e}")


# 注册路由
app.include_router(episodes.router)


@app.get("/")
async def root() -> Dict[str, Any]:
    """根路径"""
    return {
        "message": "Graphiti知识图谱API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """健康检查"""
    return {
        "status": "healthy",
        "service": "graphiti-api",
        "timestamp": ""
    }


# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail.get("message") if isinstance(exc.detail, dict) else str(exc.detail),
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    logger.error(f"未处理的异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "服务器内部错误",
            "detail": str(exc)
        }
    )


def start_server():
    """启动服务器"""
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()