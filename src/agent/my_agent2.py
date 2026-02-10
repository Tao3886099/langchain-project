from langchain.agents import create_agent
from agent.my_llm import llm
from agent.tools.tool_demo1 import web_search2
from agent.tools.tool_demo2 import MyWebSearchTool

web_search_tool = MyWebSearchTool() # 实例化自定义工具类

agent = create_agent(
    llm,
    #tools=[web_search2],
    tools=[web_search_tool],
    system_prompt="你是一个智能的助理，尽可能使用互联网搜索工具来获取最新的信息。"
)