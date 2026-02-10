from langchain.tools import tool
from openai import BaseModel
from pydantic import Field

from agent.my_llm import zhipuai_client


@tool('web_search', description="互联网搜索的工具，可以搜索所有公开的信息，并返回搜索结果。")
def web_search1(query: str) -> str:
    pass


@tool('web_search', parse_docstring=True)
def web_search2(query: str) -> str:
    """互联网搜索的工具，可以搜索所有公开的信息，并返回搜索结果。

    Args:
        query: 搜索的查询字符串。

    Returns:
        返回搜索的结果信息，该信息是一个文本字符串。
    """
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


class SearchArgs(BaseModel):
    query: str = Field(..., description="搜索的查询字符串。")

@tool('web_search', args_schema=SearchArgs , description="互联网搜索的工具，可以搜索所有公开的信息，并返回搜索结果。",parse_docstring=True)
def web_search3(query: str) -> str:
    pass

if __name__ == "__main__":
    result = web_search2.invoke({"query": "智谱AI成立于哪一年？"})
    print(result)