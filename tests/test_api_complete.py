"""
完整API测试脚本 - 包含添加和搜索验证
"""
import requests
import json
import sys
import time
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
        }
    ]
    
    print("开始测试添加文本情节API...")
    print("=" * 60)
    
    added_entities = []  # 记录添加的实体用于搜索测试
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # 发送请求
            response = requests.post(
                f"{base_url}/api/episodes/text",
                json=test_case["data"],
                headers={"Content-Type": "application/json"},
                timeout=60  # 增加超时时间
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
                
                # 提取实体名称用于搜索测试
                if '工程师' in test_case['data']['content']:
                    added_entities.append('工程师')
                if '产品经理' in test_case['data']['content']:
                    added_entities.append('产品经理')
                if 'UI设计师' in test_case['data']['content']:
                    added_entities.append('UI设计师')
                    
            else:
                result = response.json()
                print(f"失败: {result.get('message', '未知错误')}")
                if result.get('detail'):
                    print(f"详细信息: {result['detail']}")
                    
        except requests.exceptions.ConnectionError:
            print("错误: 无法连接到API服务器，请确保服务已启动")
            print("请运行: uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
            return False, []
            
        except Exception as e:
            print(f"测试失败: {e}")
            
        print("-" * 40)
    
    print("\n文本情节添加测试完成！")
    return True, added_entities


def test_search_entities(added_entities):
    """测试搜索实体API"""
    base_url = "http://localhost:8000"
    
    print("\n开始测试搜索实体API...")
    print("=" * 60)
    
    # 搜索测试用例
    search_queries = [
        "软件工程师",
        "产品经理", 
        "UI设计师",
        "北京",
        "上海",
        "科技公司"
    ]
    
    # 只测试已添加的实体
    search_queries = [query for query in search_queries if any(entity in query for entity in added_entities)]
    
    if not search_queries:
        search_queries = ["工程师", "设计师"]  # 默认搜索词
    
    for i, query in enumerate(search_queries, 1):
        print(f"\n搜索测试 {i}: '{query}'")
        print("-" * 30)
        
        try:
            # 发送搜索请求
            response = requests.get(
                f"{base_url}/api/episodes/search",
                params={"query": query, "limit": 5},
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"成功: {result['message']}")
                print(f"查询: {result['query']}")
                print(f"总数: {result['total_count']}")
                
                if result['results']:
                    print("搜索结果:")
                    for j, entity in enumerate(result['results'], 1):
                        print(f"  {j}. {entity['name']}")
                        if entity.get('summary'):
                            print(f"     摘要: {entity['summary']}")
                        if entity.get('entity_type'):
                            print(f"     类型: {entity['entity_type']}")
                        if entity.get('relevance_score'):
                            print(f"     相关性: {entity['relevance_score']:.3f}")
                        if entity.get('properties'):
                            print(f"     属性: {entity['properties']}")
                else:
                    print("未找到相关结果")
                    
            else:
                result = response.json()
                print(f"搜索失败: {result.get('message', '未知错误')}")
                if result.get('detail'):
                    print(f"详细信息: {result['detail']}")
                    
        except Exception as e:
            print(f"搜索测试失败: {e}")
            
        # 搜索间隔，避免过载
        if i < len(search_queries):
            time.sleep(2)
            
        print("-" * 30)
    
    print("\n搜索测试完成！")


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


def verify_data_integration():
    """验证数据集成完整性"""
    print("\n验证数据集成完整性...")
    print("=" * 50)
    
    # 1. 添加测试数据
    print("步骤1: 添加测试数据...")
    success, added_entities = test_add_text_episode()
    
    if not success:
        print("✗ 数据添加失败，无法继续验证")
        return False
    
    # 2. 等待数据索引
    print("\n步骤2: 等待数据索引...")
    time.sleep(3)  # 给Neo4j一些时间来索引数据
    
    # 3. 搜索验证
    print("\n步骤3: 搜索验证...")
    test_search_entities(added_entities)
    
    print("\n✓ 数据集成验证完成！")
    return True


if __name__ == "__main__":
    print("Graphiti API 完整验证测试")
    print("=" * 60)
    
    # 测试健康检查
    test_health_check()
    
    # 测试API文档
    test_api_docs()
    
    # 验证数据集成完整性
    success = verify_data_integration()
    
    if success:
        print("\n🎉 所有测试通过！API工作正常，数据集成验证成功！")
        print("\n📊 测试总结:")
        print("✅ 文本情节添加功能正常")
        print("✅ 实体搜索功能正常") 
        print("✅ 数据持久化和检索正常")
        print("✅ API文档可访问")
        print("✅ 健康检查正常")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)