"""
手动测试API端点 - 使用curl命令测试
"""
import subprocess
import json

# 测试API端点的curl命令
test_commands = [
    # 健康检查
    '''curl -X GET "http://localhost:8000/health"''',
    
    # 根路径
    '''curl -X GET "http://localhost:8000/"''',
    
    # 添加文本情节 - 完整参数
    '''curl -X POST "http://localhost:8000/api/episodes/text" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "测试员工信息", "description": "员工档案", "name": "测试档案", "reference_time": "20240104"}' ''',
    
    # 添加文本情节 - 最简参数
    '''curl -X POST "http://localhost:8000/api/episodes/text" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "简单测试内容"}' ''',
]

def run_curl_test():
    """运行curl测试"""
    print("手动测试API端点")
    print("=" * 50)
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n测试 {i}:")
        print("-" * 30)
        print(f"命令: {command}")
        print("结果:")
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print("错误:", result.stderr)
        except Exception as e:
            print(f"执行失败: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    print("请确保API服务已启动:")
    print("uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n然后按回车开始测试...")
    input()
    
    run_curl_test()