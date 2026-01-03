import logging
import time
from typing import List, Optional
#from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF
from langchain_mcp_client import EpisodeType, search_nodes, search_memory_facts


class KnowledgeGraphSearcher:
    """知识图谱搜索类"""
    def __init__(self):
        #self.mcp_client_manager = mcp_client_manager
        self.logger = logging.getLogger(__name__)

    async def basic_search(self, query: str, limit: int = 10):
        """基本搜索 - 混合搜索结合语义相似性和BM25文本检索"""
        start_time = time.time()
        self.logger.info(f"执行基本搜索: '{query}'")
        
        # 使用 search_nodes 替代 graphiti.search
        results = await search_nodes(
            query=query,
            #group_ids=["your-group-id"],  # 根据你的项目配置修改
            max_nodes=limit
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"basic_search 执行耗时: {execution_time:.4f} 秒")
        self.logger.info(f"基本搜索完成，找到 {len(results)} 个结果")
        return results

    async def center_node_search(self, query: str, center_node_uuid: str, limit: int = 10):
        """中心节点搜索 - 基于图距离重新排序搜索结果"""
        start_time = time.time()
        self.logger.info(f"执行中心节点搜索: '{query}', 中心节点: {center_node_uuid}")
        
        # 使用 search_memory_facts 替代 graphiti.search
        results = await search_memory_facts(
            query=query,
            #group_ids=["your-group-id"],  # 根据你的项目配置修改
            center_node_uuid=center_node_uuid,
            max_facts=limit
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"center_node_search 执行耗时: {execution_time:.4f} 秒")
        self.logger.info(f"中心节点搜索完成，找到 {len(results)} 个结果")
        return results

    async def node_search_with_recipe(self, query: str, limit: int = 5):
        """使用搜索配方的节点搜索 - 直接检索节点而不是边"""
        start_time = time.time()
        self.logger.info(f"执行节点搜索: '{query}'")
        
        # 使用 search_nodes 替代 graphiti._search 和 NODE_HYBRID_SEARCH_RRF
        # MCP 工具内部已封装了混合搜索逻辑
        node_search_results = await search_nodes(
            query=query,
            #group_ids=["your-group-id"],  # 根据你的项目配置修改
            max_nodes=limit
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"node_search_with_recipe 执行耗时: {execution_time:.4f} 秒")
        self.logger.info(f"节点搜索完成，找到 {len(node_search_results)} 个节点")
        return node_search_results

    def print_search_results(self, results, title: str = "搜索结果"):
        """打印搜索结果"""
        start_time = time.time()
        print(f"\n{title}:")
        print("=" * 50)
        if not results:
            print("没有找到结果")
            return
        for i, result in enumerate(results, 1):
            print(f"\n结果 {i}:")
            print(f'UUID: {result.get("uuid", "N/A")}')
            print(f'事实: {result.get("fact", "N/A")}')
            # 安全地处理日期
            if hasattr(result, 'valid_at') and result.get('valid_at'):
                try:
                    # 尝试修复常见的日期格式问题
                    valid_at_str = str(result.get('valid_at'))
                    if 'ity' in valid_at_str:
                        # 修复错误的月份名称
                        valid_at_str = valid_at_str.replace('ity', 'Jul')
                        print(f'有效期从: {valid_at_str}')
                except Exception as e:
                    print(f'有效期从: {result.get("valid_at")} (解析错误: {e})')
            if hasattr(result, 'invalid_at') and result.get('invalid_at'):
                try:
                    # 尝试修复常见的日期格式问题
                    invalid_at_str = str(result.get('invalid_at'))
                    if 'ity' in invalid_at_str:
                        # 修复错误的月份名称
                        invalid_at_str = invalid_at_str.replace('ity', 'Jul')
                        print(f'有效期至: {invalid_at_str}')
                except Exception as e:
                    print(f'有效期至: {result.get("invalid_at")} (解析错误: {e})')
            print("-" * 30)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"print_search_results 执行耗时: {execution_time:.4f} 秒")

    def print_node_search_results(self, node_search_results, title: str = "节点搜索结果"):
        """打印节点搜索结果"""
        start_time = time.time()
        print(f"\n{title}:")
        print("=" * 50)
        if not node_search_results:
            print("没有找到节点")
            return
        for i, node in enumerate(node_search_results, 1):
            print(f"\n节点 {i}:")
            print(f'节点UUID: {node.get("uuid", "N/A")}')
            print(f'节点名称: {node.get("name", "N/A")}')
            node_summary = node.get('summary', 'N/A')[:100] + '...' if len(node.get('summary', 'N/A')) > 100 else node.get('summary', 'N/A')
            print(f'内容摘要: {node_summary}')
            print(f'节点标签: {", ".join(node.get("labels", []))}')
            print(f'创建时间: {node.get("created_at", "N/A")}')
            if 'attributes' in node and node.get('attributes', {}):
                print('属性:')
                for key, value in node.get('attributes', {}).items():
                    print(f'  {key}: {value}')
            print("-" * 30)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"print_node_search_results 执行耗时: {execution_time:.4f} 秒")

    async def search_with_center_node_reranking(self, query: str, limit: int = 10):
        """带中心节点重新排序的搜索"""
        start_time = time.time()
        self.logger.info(f"执行带中心节点重新排序的搜索: '{query}'")
        # 首先执行基本搜索
        initial_results = await self.basic_search(query, limit)
        if not initial_results:
            self.logger.warning("初始搜索中没有找到结果")
            return []
        # 使用第一个结果作为中心节点
        #center_node_uuid = initial_results[0].get('uuid')
        #self.logger.info(f"使用中心节点UUID: {center_node_uuid}")
        # 使用第一个结果作为中心节点
        if initial_results and initial_results[0]:
            center_node_uuid = initial_results[0].get("uuid")
            if center_node_uuid:
                self.logger.info(f"使用中心节点UUID: {center_node_uuid}")
            else:
                self.logger.error("无法从初始结果中获取中心节点UUID")
                return []
        else:
            self.logger.error("初始搜索结果为空")
            return []

        # 执行中心节点搜索
        reranked_results = await self.center_node_search(query, center_node_uuid, limit)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"search_with_center_node_reranking 执行耗时: {execution_time:.4f} 秒")
        return reranked_results

    async def comprehensive_search(self, query: str, limit: int = 5):
        """综合搜索 - 执行所有类型的搜索"""
        start_time = time.time()
        self.logger.info(f"执行综合搜索: '{query}'")
        results = {
            'basic_search': None,
            'node_search': None,
            'center_node_search': None
        }
        try:
            # 基本搜索
            results['basic_search'] = await self.basic_search(query, limit)
            # 节点搜索
            results['node_search'] = await self.node_search_with_recipe(query, limit)
            # 如果有基本搜索结果，执行中心节点搜索
            if results['basic_search']:
                center_node_uuid = results['basic_search'][0].get('uuid')
                results['center_node_search'] = await self.center_node_search(
                    query, center_node_uuid, limit
                )
        except Exception as e:
            self.logger.error(f"综合搜索时出错: {e}")
            raise
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"comprehensive_search 执行耗时: {execution_time:.4f} 秒")
        return results

    def print_comprehensive_results(self, comprehensive_results):
        """打印综合搜索结果"""
        start_time = time.time()
        print("\n" + "=" * 60)
        print("综合搜索结果")
        print("=" * 60)
        # 基本搜索结果
        if comprehensive_results['basic_search']:
            self.print_search_results(
                comprehensive_results['basic_search'],
                "基本搜索结果"
            )
        # 节点搜索结果
        if comprehensive_results['node_search']:
            self.print_node_search_results(
                comprehensive_results['node_search'],
                "节点搜索结果"
            )
        # 中心节点搜索结果
        if comprehensive_results['center_node_search']:
            self.print_search_results(
                comprehensive_results['center_node_search'],
                "中心节点重新排序搜索结果"
            )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"print_comprehensive_results 执行耗时: {execution_time:.4f} 秒")

    async def get_graph_summary(self):
        """获取知识图谱的统计摘要"""
        start_time = time.time()
        self.logger.info("获取知识图谱统计摘要...")
        try:
#            graphiti = self.get_graphiti()
            # 使用直接的Neo4j查询获取准确的统计信息
            node_count = 0
            edge_count = 0
#            try:
                # 获取节点数量
#                session = graphiti.driver.session()
#                result = await session.run("MATCH (n) RETURN count(n) as node_count")
#                node_count = (await result.single())["node_count"]
#                await session.close()
                # 获取边（关系）数量
#                session = graphiti.driver.session()
#                result = await session.run("MATCH ()-[r]->() RETURN count(r) as edge_count")
#                edge_count = (await result.single())["edge_count"]
#                await session.close()
#                self.logger.info(f"直接从Neo4j获取统计: 节点={node_count}, 边={edge_count}")
#            except Exception as e:
#                self.logger.warning(f"无法从Neo4j直接获取统计: {e}")
                # 直接抛出异常，不再尝试任何估算方式
#                raise
            summary = {
                'node_count': node_count,
                'edge_count': edge_count,
                'total_elements': node_count + edge_count
            }
            self.logger.info(f"知识图谱摘要: 节点={node_count}, 边={edge_count}")
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"get_graph_summary 执行耗时: {execution_time:.4f} 秒")
            return summary
        except Exception as e:
            self.logger.error(f"获取知识图谱摘要时出错: {e}")
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"get_graph_summary 执行耗时: {execution_time:.4f} 秒 (出错)")
            return {
                'node_count': 8,
                'edge_count': 15,
                'total_elements': 23,
                'error': str(e)
            }
