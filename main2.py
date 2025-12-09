import asyncio
import logging
import time
from neo4j_connector import Neo4jConnector
from ollama_graphiti_manager import OllamaGraphitiManager
from knowledge_graph_builder import KnowledgeGraphBuilder
from knowledge_graph_searcher import KnowledgeGraphSearcher
from graphiti_core.nodes import EpisodeType
from config import config
# 设置全面的日志配置
try:
 from log_config import setup_comprehensive_logging
    setup_comprehensive_logging()
except ImportError:
 # 如果配置文件不存在，使用默认设置
    logging.getLogger('graphiti_core.utils.maintenance.edge_operations').setLevel(logging.ERROR)
    logging.getLogger('graphiti_core.driver.neo4j_driver').setLevel(logging.WARNING)
    logging.getLogger('graphiti_core').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
class KnowledgeGraphTestApplication:
 """知识图谱测试应用主类"""
 def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.neo4j_connector = None
        self.graphiti_manager = None
        self.graph_builder = None
        self.searcher = None
 async def initialize(self):
 """初始化应用"""
        start_time = time.time()
        self.logger.info("初始化知识图谱应用...")
 try:
 # 子步骤1: 初始化Neo4j连接
            step_start = time.time()
            self.logger.info("子步骤1: 初始化Neo4j连接...")
            neo4j_config = config.get_neo4j_config()
            self.neo4j_connector = Neo4jConnector(
                uri=neo4j_config['uri'],
                user=neo4j_config['user'],
                password=neo4j_config['password']
            )
            self.neo4j_connector.validate_connection()
            self.logger.info("Neo4j连接器初始化完成")
            step_end = time.time()
 print(f"Neo4j连接初始化耗时: {step_end - step_start:.2f} 秒")
 # 子步骤2: 初始化Ollama和Graphiti管理器
            step_start = time.time()
            self.logger.info("子步骤2: 初始化Ollama和Graphiti管理器...")
            self.graphiti_manager = OllamaGraphitiManager(self.neo4j_connector)
 await self.graphiti_manager.initialize_graphiti()
 await self.graphiti_manager.setup_database()
            self.logger.info("Ollama和Graphiti管理器初始化完成")
            step_end = time.time()
 print(f"Ollama和Graphiti管理器初始化耗时: {step_end - step_start:.2f} 秒")
 # 子步骤3: 初始化知识图谱构建器
            step_start = time.time()
            self.logger.info("子步骤3: 初始化知识图谱构建器...")
            self.graph_builder = KnowledgeGraphBuilder(self.graphiti_manager)
            self.logger.info("知识图谱构建器初始化完成")
            step_end = time.time()
 print(f"知识图谱构建器初始化耗时: {step_end - step_start:.2f} 秒")
 # 子步骤4: 初始化搜索器
            step_start = time.time()
            self.logger.info("子步骤4: 初始化搜索器...")
            self.searcher = KnowledgeGraphSearcher(self.graphiti_manager)
            self.logger.info("搜索器初始化完成")
            step_end = time.time()
 print(f"搜索器初始化耗时: {step_end - step_start:.2f} 秒")
            self.logger.info("应用初始化完成")
            total_time = time.time() - start_time
 print(f"应用初始化总耗时: {total_time:.2f} 秒")
 except Exception as e:
            self.logger.error(f"应用初始化失败: {e}")
 raise
 async def build_knowledge_graph(self):
 """构建知识图谱"""
        start_time = time.time()
        self.logger.info("开始构建知识图谱...")
 try:
 # 构建步骤1: 添加示例情节
            step_start = time.time()
            self.logger.info("构建步骤1: 添加示例情节...")
 # 创建示例数据
            sample_episodes = [
                self.graph_builder.create_text_episode(
 "张三是一名软件工程师，他在北京的一家科技公司工作。他主要负责前端开发，使用React和TypeScript技术栈。他毕业于清华大学计算机科学专业。",
 "员工档案信息"
                ),
                self.graph_builder.create_text_episode(
 "李四是张三的同事，她是一名后端工程师，专门负责数据库设计和API开发。她使用Java和Spring Boot框架，有5年的工作经验。",
 "员工档案信息"
                ),
                self.graph_builder.create_json_episode(
                    {
 'name': '王五',
 'position': '技术总监',
 'company': '北京科技有限公司',
 'department': '技术部',
 'experience': '10年',
 'skills': ['Java', 'Python', '微服务架构', '团队管理']
                    },
 "员工详细信息"
                ),
                self.graph_builder.create_json_episode(
                    {
 'name': '赵六',
 'position': '产品经理',
 'company': '北京科技有限公司',
 'department': '产品部',
 'projects': ['用户管理系统', '数据分析平台'],
 'experience': '8年'
                    },
 "员工详细信息"
                )
            ]
 await self.graph_builder.add_episodes(sample_episodes)
            self.logger.info("构建步骤1: 示例情节添加完成")
            step_end = time.time()
 print(f"示例情节添加耗时: {step_end - step_start:.2f} 秒")
            self.logger.info("知识图谱构建完成")
            total_time = time.time() - start_time
 print(f"知识图谱构建总耗时: {total_time:.2f} 秒")
 except Exception as e:
            self.logger.error(f"构建知识图谱时出错: {e}")
 raise
 async def test_case_1_add_nodes_and_edges(self):
 """测试用例1: 在原有知识图谱上新增节点和边，展示差异"""
        total_start_time = time.time()
        self.logger.info("开始测试用例1: 新增节点和边...")
 try:
 # 获取原始知识图谱状态
            step_start = time.time()
            self.logger.info("获取原始知识图谱状态...")
            original_graph = await self.searcher.get_graph_summary()
            step_end = time.time()
 print(f"获取原始知识图谱状态耗时: {step_end - step_start:.2f} 秒")
 print(f"\n{'='*20} 测试用例1: 新增节点和边 {'='*20}")
 print("原始知识图谱状态:")
 print(f"节点数量: {original_graph.get('node_count', 0)}")
 print(f"边数量: {original_graph.get('edge_count', 0)}")
 # 添加新的节点和边
            self.logger.info("添加新的节点和边...")
 # 添加新员工信息
            step_start = time.time()
            new_employee_data = {
 'name': '李九',
 'position': '产品经理',
 'company': '北京科技有限公司',
 'department': '产品部',
 'experience': '8年',
 'skills': ['产品规划', '用户调研', '数据分析', '项目管理']
            }
 try:
 await self.graph_builder.add_json_episode(
                    json_data=new_employee_data,
                    description="新增员工详细信息",
                    name="李九详细信息"
                )
 print("李九信息添加成功")
 except Exception as e:
 print(f"李九信息添加失败: {e}")
 # 如果JSON方式失败，使用文本方式
 await self.graph_builder.add_single_episode(
                    content="李九是一名产品经理，在北京科技有限公司产品部工作，有8年经验，掌握产品规划、用户调研、数据分析、项目管理等技能。",
                    episode_type=EpisodeType.text,
                    description="新增员工详细信息",
                    name="李九详细信息文本版"
                )
 print("使用文本方式添加李九信息成功")
            step_end = time.time()
 print(f"添加李九信息耗时: {step_end - step_start:.2f} 秒")
 # 添加项目信息
            step_start = time.time()
            project_data = {
 'name': '智能客服系统',
 'type': 'AI项目',
 'status': '进行中',
 'team_members': ['李九', '张三', '王五'],
 'technologies': ['Python', 'TensorFlow', 'React', 'Neo4j']
            }
 try:
 await self.graph_builder.add_json_episode(
                    json_data=project_data,
                    description="项目详细信息",
                    name="智能客服系统项目"
                )
 print("智能客服系统项目信息添加成功")
 except Exception as e:
 print(f"智能客服系统项目信息添加失败: {e}")
 # 如果JSON方式失败，使用文本方式
 await self.graph_builder.add_single_episode(
                    content="智能客服系统是一个AI项目，状态为进行中，团队成员包括李九、张三、王五，使用Python、TensorFlow、React、Neo4j等技术。",
                    episode_type=self.graph_builder.get_sample_episodes()[0]['type'],
                    description="项目详细信息",
                    name="智能客服系统项目文本版"
                )
 print("使用文本方式添加项目信息成功")
            step_end = time.time()
 print(f"添加项目信息耗时: {step_end - step_start:.2f} 秒")
 # 获取更新后的知识图谱状态
            step_start = time.time()
            self.logger.info("获取更新后的知识图谱状态...")
            updated_graph = await self.searcher.get_graph_summary()
            step_end = time.time()
 print(f"获取更新后知识图谱状态耗时: {step_end - step_start:.2f} 秒")
 print("\n更新后的知识图谱状态:")
 print(f"节点数量: {updated_graph.get('node_count', 0)}")
 print(f"边数量: {updated_graph.get('edge_count', 0)}")
 # 计算差异
            node_diff = updated_graph.get('node_count', 0) - original_graph.get('node_count', 0)
            edge_diff = updated_graph.get('edge_count', 0) - original_graph.get('edge_count', 0)
 print(f"\n知识图谱差异分析:")
 print(f"新增节点数量: {node_diff}")
 print(f"新增边数量: {edge_diff}")
 # 搜索新增的内容
            step_start = time.time()
 print(f"\n搜索新增的员工信息:")
            new_employee_results = await self.searcher.basic_search('李九')
            self.searcher.print_search_results(new_employee_results, "新增员工搜索结果")
            step_end = time.time()
 print(f"搜索李九信息耗时: {step_end - step_start:.2f} 秒")
            step_start = time.time()
 print(f"\n搜索新增的项目信息:")
            new_project_results = await self.searcher.basic_search('智能客服系统')
            self.searcher.print_search_results(new_project_results, "新增项目搜索结果")
            step_end = time.time()
 print(f"搜索项目信息耗时: {step_end - step_start:.2f} 秒")
 # 计算执行耗时
            total_end_time = time.time()
            total_execution_time = total_end_time - total_start_time
 print(f"\n测试用例1总执行耗时: {total_execution_time:.2f} 秒")
            self.logger.info(f"测试用例1完成，耗时: {total_execution_time:.2f} 秒")
 except Exception as e:
 # 即使出错也要计算耗时
            total_end_time = time.time()
            total_execution_time = total_end_time - total_start_time
 print(f"\n测试用例1执行失败，耗时: {total_execution_time:.2f} 秒")
            self.logger.error(f"测试用例1执行时出错: {e}")
 raise
 async def test_case_2_modify_node_attributes(self):
 """测试用例2: 修改节点属性，展示差异"""
        total_start_time = time.time()
        self.logger.info("开始测试用例2: 修改节点属性...")
 try:
 print(f"\n{'='*20} 测试用例2: 修改节点属性 {'='*20}")
 # 获取原始知识图谱状态
            step_start = time.time()
            self.logger.info("获取原始知识图谱状态...")
            original_graph = await self.searcher.get_graph_summary()
            step_end = time.time()
 print(f"获取原始知识图谱状态耗时: {step_end - step_start:.2f} 秒")
 print("修改前的知识图谱状态:")
 print(f"节点数量: {original_graph.get('node_count', 0)}")
 print(f"边数量: {original_graph.get('edge_count', 0)}")
 # 搜索张三的原始信息
            step_start = time.time()
 print(f"\n搜索张三的原始信息:")
            original_zhang_san = await self.searcher.basic_search('张三')
            self.searcher.print_search_results(original_zhang_san, "张三原始信息")
            step_end = time.time()
 print(f"搜索张三原始信息耗时: {step_end - step_start:.2f} 秒")
 # 添加张三的更新信息（使用更简单的数据结构）
            step_start = time.time()
            self.logger.info("添加张三的更新信息...")
 # 首先尝试使用最简单的文本方式，避免JSON解析问题
 try:
 await self.graph_builder.add_single_episode(
                    content="张三已晋升为高级软件工程师，经验增加到5年，掌握Java、Spring Boot、微服务架构等技能，薪资25000元，绩效评级优秀。",
                    episode_type=self.graph_builder.get_sample_episodes()[0]['type'],
                    description="员工信息更新",
                    name="张三信息更新文本版"
                )
 print("使用文本方式更新张三信息成功")
                json_update_success = False
 except Exception as e:
 print(f"文本方式更新失败: {e}")
                json_update_success = False
 # 如果文本方式失败，尝试JSON方式
 if not json_update_success:
 try:
 # 使用更简单的数据结构，避免复杂的嵌套
                    updated_zhang_san_data = {
 'name': '张三',
 'position': '高级软件工程师',
 'company': '北京科技有限公司',
 'department': '技术部',
 'experience': '5年',
 'skills': ['Java', 'Spring Boot', '微服务架构']
                    }
 await self.graph_builder.add_json_episode(
                        json_data=updated_zhang_san_data,
                        description="员工信息更新",
                        name="张三信息更新JSON版"
                    )
 print("使用JSON方式更新张三信息成功")
 except Exception as e:
 print(f"JSON方式更新也失败: {e}")
 print("跳过张三信息更新，继续执行后续步骤")
            step_end = time.time()
 print(f"更新张三信息耗时: {step_end - step_start:.2f} 秒")
 # 获取更新后的知识图谱状态
            step_start = time.time()
            self.logger.info("获取更新后的知识图谱状态...")
            updated_graph = await self.searcher.get_graph_summary()
            step_end = time.time()
 print(f"获取更新后知识图谱状态耗时: {step_end - step_start:.2f} 秒")
 print("\n修改后的知识图谱状态:")
 print(f"节点数量: {updated_graph.get('node_count', 0)}")
 print(f"边数量: {updated_graph.get('edge_count', 0)}")
 # 计算差异
            node_diff = updated_graph.get('node_count', 0) - original_graph.get('node_count', 0)
            edge_diff = updated_graph.get('edge_count', 0) - original_graph.get('edge_count', 0)
 print(f"\n知识图谱差异分析:")
 print(f"节点数量变化: {node_diff}")
 print(f"边数量变化: {edge_diff}")
 print("注意: 属性修改不会新增节点，但会创建新的关系")
 # 搜索更新后的张三信息
            step_start = time.time()
 print(f"\n搜索张三的更新信息:")
            updated_zhang_san = await self.searcher.basic_search('张三')
            self.searcher.print_search_results(updated_zhang_san, "张三更新信息")
            step_end = time.time()
 print(f"搜索张三更新信息耗时: {step_end - step_start:.2f} 秒")
 # 搜索新增的技能信息
            step_start = time.time()
 print(f"\n搜索新增的技能信息:")
            skills_results = await self.searcher.basic_search('微服务架构')
            self.searcher.print_search_results(skills_results, "新增技能搜索结果")
            step_end = time.time()
 print(f"搜索技能信息耗时: {step_end - step_start:.2f} 秒")
 # 搜索薪资信息
            step_start = time.time()
 print(f"\n搜索薪资信息:")
            salary_results = await self.searcher.basic_search('25000')
            self.searcher.print_search_results(salary_results, "薪资信息搜索结果")
            step_end = time.time()
 print(f"搜索薪资信息耗时: {step_end - step_start:.2f} 秒")
 # 搜索绩效信息
            step_start = time.time()
 print(f"\n搜索绩效信息:")
            performance_results = await self.searcher.basic_search('优秀')
            self.searcher.print_search_results(performance_results, "绩效信息搜索结果")
            step_end = time.time()
 print(f"搜索绩效信息耗时: {step_end - step_start:.2f} 秒")
 # 计算执行耗时
            total_end_time = time.time()
            total_execution_time = total_end_time - total_start_time
 print(f"\n测试用例2总执行耗时: {total_execution_time:.2f} 秒")
            self.logger.info(f"测试用例2完成，耗时: {total_execution_time:.2f} 秒")
 except Exception as e:
 # 即使出错也要计算耗时
            total_end_time = time.time()
            total_execution_time = total_end_time - total_start_time
 print(f"\n测试用例2执行失败，耗时: {total_execution_time:.2f} 秒")
            self.logger.error(f"测试用例2执行时出错: {e}")
 raise
 async def cleanup(self):
 """清理资源"""
        start_time = time.time()
        self.logger.info("开始清理资源...")
 try:
 # 清理步骤1: 关闭Graphiti连接
            step_start = time.time()
            self.logger.info("清理步骤1: 关闭Graphiti连接...")
 if self.graphiti_manager:
 await self.graphiti_manager.close_connection()
                self.logger.info("清理步骤1: Graphiti连接已关闭")
 else:
                self.logger.info("清理步骤1: 跳过Graphiti连接关闭（管理器未初始化）")
            step_end = time.time()
 print(f"关闭Graphiti连接耗时: {step_end - step_start:.2f} 秒")
            self.logger.info("资源清理完成")
            total_time = time.time() - start_time
 print(f"资源清理总耗时: {total_time:.2f} 秒")
 except Exception as e:
            self.logger.error(f"清理资源时出错: {e}")
 async def run_tests(self):
 """运行测试用例"""
        total_start_time = time.time()
 try:
 # 步骤1: 初始化
            step_start = time.time()
            self.logger.info("步骤1: 开始初始化应用...")
 print(f"\n{'='*20} 步骤1: 初始化应用 {'='*20}")
 await self.initialize()
            self.logger.info("步骤1: 初始化完成")
 print(f"步骤1: 初始化完成")
            step_end = time.time()
 print(f"步骤1总耗时: {step_end - step_start:.2f} 秒")
 # 步骤2: 构建知识图谱
            step_start = time.time()
            self.logger.info("步骤2: 开始构建知识图谱...")
 print(f"\n{'='*20} 步骤2: 构建知识图谱 {'='*20}")
 await self.build_knowledge_graph()
            self.logger.info("步骤2: 知识图谱构建完成")
 print(f"步骤2: 知识图谱构建完成")
            step_end = time.time()
 print(f"步骤2总耗时: {step_end - step_start:.2f} 秒")
 # 步骤3: 测试用例1 - 新增节点和边
            step_start = time.time()
            self.logger.info("步骤3: 开始测试用例1...")
 await self.test_case_1_add_nodes_and_edges()
            self.logger.info("步骤3: 测试用例1完成")
 print(f"步骤3: 测试用例1完成")
            step_end = time.time()
 print(f"步骤3总耗时: {step_end - step_start:.2f} 秒")
 # 步骤4: 测试用例2 - 修改节点属性
            step_start = time.time()
            self.logger.info("步骤4: 开始测试用例2...")
 await self.test_case_2_modify_node_attributes()
            self.logger.info("步骤4: 测试用例2完成")
 print(f"步骤4: 测试用例2完成")
            step_end = time.time()
 print(f"步骤4总耗时: {step_end - step_start:.2f} 秒")
            self.logger.info("所有测试用例完成")
            total_end_time = time.time()
            total_time = total_end_time - total_start_time
 print(f"\n所有测试用例总耗时: {total_time:.2f} 秒")
 print(f"\n所有 4 个步骤都已完成！")
 except Exception as e:
            self.logger.error(f"测试过程中出错: {e}")
 print(f"\n测试失败: {e}")
 raise
 finally:
 # 步骤5: 清理资源
            step_start = time.time()
            self.logger.info("步骤5: 开始清理资源...")
 print(f"\n{'='*20} 步骤5: 清理资源 {'='*20}")
 await self.cleanup()
            self.logger.info("步骤5: 资源清理完成")
 print(f"步骤5: 资源清理完成")
            step_end = time.time()
 print(f"步骤5总耗时: {step_end - step_start:.2f} 秒")
async def main():
 """主函数"""
 print("=" * 60)
 print("知识图谱测试应用")
 print("=" * 60)
    app = KnowledgeGraphTestApplication()
 try:
 await app.run_tests()
 print("\n" + "=" * 60)
 print("测试成功完成！")
 print("=" * 60)
 except Exception as e:
 print(f"\n测试失败: {e}")
 raise
if __name__ == "__main__":
    asyncio.run(main()) 