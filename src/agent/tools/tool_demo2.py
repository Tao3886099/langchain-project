from typing import Type

from langchain_core.tools import BaseTool
from agent.my_llm import zhipuai_client
from pydantic import BaseModel, Field, create_model


class SearchArgs(BaseModel): #类：数据结构体
    query: str = Field(..., description="搜索的查询字符串。")

class MyWebSearchTool(BaseTool):
    name: str = "web_search_byClass"
    description: str = "互联网搜索的工具，可以搜索所有公开的信息，并返回搜索结果。"
    #工具的参数结构体，第一种写法
    #args_schema: Type[BaseModel] = SearchArgs

    #工具的参数结构体，第二种写法
    def __init__(self):
        super().__init__()
        self.args_schema = create_model("searchInput",query=(str, Field(..., description="搜索的查询字符串。")))

    def _run(self, query: str) -> str:
        try:
            resp = zhipuai_client.web_search.web_search(
                search_engine="search_pro",
                search_query=query
            )
            if resp.search_result:
                return "\n".join([d.content for d in resp.search_result])
            return "未找到相关搜索结果。"
        except Exception as e:
            print(e)
            return f"搜索时出错: {e}"
