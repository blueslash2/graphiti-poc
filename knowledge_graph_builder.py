import json
import logging
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Union
from langchain_mcp_client import EpisodeType, add_episode


class KnowledgeGraphBuilder:
    """通用知识图谱构建类"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_episode_data(
        self,
        content: Union[str, Dict[str, Any]],
        episode_type: EpisodeType = EpisodeType.text,
        description: str = "通用信息",
        name: str = None
    ) -> Dict[str, Any]:
        """创建通用情节数据"""
        start_time = time.time()
        if name is None:
            name = f"情节_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        result = {
            'content': content,
            'type': episode_type,
            'description': description,
            'name': name
            }
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_episode_data 执行耗时: {execution_time:.4f} 秒")
        return result

    def create_text_episode(
        self,
        text_content: str,
        description: str = "文本信息",
        name: str = None
    ) -> Dict[str, Any]:
        """创建文本情节数据"""
        start_time = time.time()
        result = self.create_episode_data(
            content=text_content,
            episode_type=EpisodeType.text,
            description=description,
            name=name
            )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_text_episode 执行耗时: {execution_time:.4f} 秒")
        return result

    def create_json_episode(self, json_data: Dict[str, Any], description: str = "结构化信息",
                           name: str = None) -> Dict[str, Any]:
        """创建JSON情节数据"""
        start_time = time.time()
        result = self.create_episode_data(
            content=json_data,
            episode_type=EpisodeType.json,
            description=description,
            name=name
            )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_json_episode 执行耗时: {execution_time:.4f} 秒")
        return result

    def convert_json_to_text(self, json_data: Dict[str, Any]) -> str:
        """将JSON数据转换为自然语言文本"""
        start_time = time.time()
        content_parts = []
        for key, value in json_data.items():
            if value is not None:
                if isinstance(value, list):
                    value_str = '、'.join(str(item) for item in value)
                else:
                    value_str = str(value)
            content_parts.append(f"{key}是{value_str}")
        result = '，'.join(content_parts) + '。'
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"convert_json_to_text 执行耗时: {execution_time:.4f} 秒")
        return result

    async def add_episodes(self, episodes: List[Dict[str, Any]]):
        """添加多个情节到知识图谱"""
        start_time = time.time()
        if not episodes:
            self.logger.warning("没有提供情节数据")
            return
        self.logger.info(f"开始添加 {len(episodes)} 个情节...")
        for i, episode in enumerate(episodes):
            episode_start_time = time.time()
            try:
                content = episode['content']
                episode_type = episode['type']
                description = episode.get('description', '通用信息')
                name = episode.get('name', f'情节_{i}')
                # 处理内容格式
                if episode_type == EpisodeType.json and isinstance(content, dict):
                    # JSON数据转换为文本
                    episode_body = self.convert_json_to_text(content)
                elif isinstance(content, str):
                    episode_body = content
                else:
                    # 其他情况转换为JSON字符串
                    episode_body = json.dumps(content, ensure_ascii=False)
                # 2. 改为直接调用新的 add_episode 函数
                await add_episode(
                    name=name,
                    episode_body=episode_body,
                    source=episode_type,
                    source_description=description,
                    # reference_time=datetime.now(timezone.utc),  # 如果需要可取消注释
                )
                # 兼容 episode_type 可能是枚举或字符串
                type_label = episode_type.value if hasattr(episode_type, "value") else episode_type
                self.logger.info(f'已添加情节: {name} ({type_label})')
                episode_end_time = time.time()
                episode_execution_time = episode_end_time - episode_start_time
                print(f"添加情节 {i+1} ({name}) 耗时: {episode_execution_time:.4f} 秒")
            except Exception as e:
                self.logger.error(f"添加情节 {i} 时出错: {e}")
                raise
        end_time = time.time() #因为有for 所以不能用finally保证计时器
        total_execution_time = end_time - start_time
        print(f"add_episodes 总执行耗时: {total_execution_time:.4f} 秒")
        self.logger.info("所有情节添加完成")

    async def add_single_episode(self, content: Union[str, Dict[str, Any]], 
                                episode_type: EpisodeType = EpisodeType.text,
                                description: str = "通用信息", 
                                name: str = None):
        """添加单个情节"""
        start_time = time.time()
        if name is None:
            name = f"情节_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            # 处理内容格式
            if episode_type == EpisodeType.json and isinstance(content, dict):
                episode_body = self.convert_json_to_text(content)
            elif isinstance(content, str):
                episode_body = content
            else:
                episode_body = json.dumps(content, ensure_ascii=False)
            # 3. 改为直接调用新的 add_episode 函数
            await add_episode(
                name=name,
                episode_body=episode_body,
                source=episode_type,
                source_description=description,
                reference_time=datetime.now(timezone.utc),
            )
            self.logger.info(f'已添加情节: {name}')
        except Exception as e:
            self.logger.error(f"添加情节时出错: {e}")
            raise
        finally:
            end_time = time.time() #防止raise影响计时器
            execution_time = end_time - start_time
            print(f"add_single_episode 执行耗时: {execution_time:.4f} 秒")

    async def add_json_episode(self, json_data: Dict[str, Any], 
                              description: str = "结构化信息", 
                              name: str = None):
        """添加JSON格式的情节"""
        start_time = time.time()
        await self.add_single_episode(
            content=json_data,
            episode_type=EpisodeType.json,
            description=description,
            name=name
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"add_json_episode 执行耗时: {execution_time:.4f} 秒")

    def create_episode_batch(self, data_list: List[Dict[str, Any]], 
                            episode_type: EpisodeType = EpisodeType.text,
                            description: str = "批量信息") -> List[Dict[str, Any]]:
        """批量创建情节数据"""
        start_time = time.time()
        episodes = []
        for i, data in enumerate(data_list):
            episode = self.create_episode_data(
                content=data,
                episode_type=episode_type,
                description=description,
                name=f"批量情节_{i+1}"
            )
            episodes.append(episode)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_episode_batch 执行耗时: {execution_time:.4f} 秒")
        return episodes

    def create_text_episode_batch(self, text_list: List[str], 
                                 description: str = "批量文本信息") -> List[Dict[str, Any]]:
        """批量创建文本情节数据"""
        start_time = time.time()
        result = self.create_episode_batch(
            data_list=text_list,
            episode_type=EpisodeType.text,
            description=description
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_text_episode_batch 执行耗时: {execution_time:.4f} 秒")
        return result

    def create_json_episode_batch(self, json_list: List[Dict[str, Any]], 
                                 description: str = "批量结构化信息") -> List[Dict[str, Any]]:
        """批量创建JSON情节数据"""
        start_time = time.time()
        result = self.create_episode_batch(
            data_list=json_list,
            episode_type=EpisodeType.json,
            description=description
        )
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"create_json_episode_batch 执行耗时: {execution_time:.4f} 秒")
        return result
