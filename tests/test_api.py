"""
API测试脚本
"""
import requests
import json
import sys
from datetime import datetime


def test_add_text_episode():
    """测试添加文本情节API"""
    base_url = "http://localhost:8000"
    
    # 测试数据
    test_cases = [
        {
            "name": "完整参数测试",
            "data": {
                "content": "李四是一名产品经理，在上海的互联网公司工作，主要负责产品规划和用户体验设计。她有5年的产品经验，毕业于复旦大学。",
                "description": "员工档案信息",
                "name": "李四档案",
                "reference_time": "20240104"
            }
        },
        {
            "name": "最简参数测试",
            "data": {
                "content": "王五是一名后端工程师，专注于微服务架构设计。"
            }
        },
        {
            "name": "年月格式测试",
            "data": {
                "content": "赵六是一名UI设计师，擅长用户体验设计和界面美化。",
                "reference_time": "202401"
            }
        },
        {
            "name": "长文本测试",
            "data": {
                "content": """张三是一名资深全栈工程师，在北京某知名科技公司担任技术负责人。他拥有10年的软件开发经验，
                精通多种编程语言包括Java、Python、JavaScript等。他毕业于清华大学计算机科学专业，
                曾在多家知名互联网公司工作，参与过多个大型项目的架构设计和开发。
                
                在技术方面，张三擅长微服务架构设计、分布式系统开发、性能优化等。他熟悉Spring Boot、
                Django、React等主流开发框架，对云计算、大数据、人工智能等前沿技术也有深入研究。
                
                除了技术能力，张三还具备良好的团队协作能力和项目管理经验。他曾带领团队完成多个重要项目，
                在敏捷开发、代码审查、技术分享等方面都有丰富经验。""",
                "description": "详细员工信息",
                "name": "张三详细档案"
            }
        }
    ]
    
    print("开始测试添加文本情节API...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # 发送请求
            response = requests.post(
                f"{base_url}/api/episodes/text",
                json=test_case["data"],
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"成功: {result['message']}")
                print(f"情节名称: {result['data']['name']}")
                print(f"描述: {result['data']['description']}")
                print(f"内容预览: {result['data']['content_preview']}")
                if result['data'].get('reference_time'):
                    print(f"参考时间: {result['data']['reference_time']}")
            else:
                result = response.json()
                print(f"失败: {result.get('message', '未知错误')}")
                if result.get('detail'):
                    print(f"详细信息: {result['detail']}")
                    
        except requests.exceptions.ConnectionError:
            print("错误: 无法连接到API服务器，请确保服务已启动")
            print("请运行: uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
            return False
            
        except Exception as e:
            print(f"测试失败: {e}")
            
        print("-" * 40)
    
    print("\n测试完成！")
    return True


def test_health_check():
    """测试健康检查端点"""
    base_url = "http://localhost:8000"
    
    print("\n测试健康检查端点...")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"健康检查状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"服务状态: {result['status']}")
            print(f"服务名称: {result['service']}")
        else:
            print(f"健康检查失败: {response.text}")
            
    except Exception as e:
        print(f"健康检查失败: {e}")


def test_api_docs():
    """测试API文档"""
    base_url = "http://localhost:8000"
    
    print("\n测试API文档...")
    print("-" * 20)
    
    docs_urls = ["/docs", "/redoc"]
    
    for docs_url in docs_urls:
        try:
            response = requests.get(f"{base_url}{docs_url}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {docs_url} 可访问")
            else:
                print(f"✗ {docs_url} 无法访问")
        except Exception as e:
            print(f"✗ {docs_url} 访问失败: {e}")


if __name__ == "__main__":
    print("Graphiti API 测试脚本")
    print("=" * 60)
    
    # 测试健康检查
    test_health_check()
    
    # 测试API文档
    test_api_docs()
    
    # 测试添加文本情节
    success = test_add_text_episode()
    
    if success:
        print("\n✓ 所有测试完成！")
        sys.exit(0)
    else:
        print("\n✗ 测试失败！")
        sys.exit(1)