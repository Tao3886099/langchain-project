from typing import List

from langchain.agents import create_agent
from langchain_core.tools import BaseTool

from agent.my_llm import llm
from agent.tools.test_to_sql_tools import SQLQueryTool, SQLQueryValidationTool, ListTablesTool, TableSchemaTool
from agent.utils.db_utils import MySQLDataBaseManager

DB_CONFIG = {
        "host": "139.159.228.234",
        "port": 3306,
        "user": "root",
        "password": "Tao3886099",
        "database": "ry-vue"
    }
connection = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"

def get_tools(connection: str) -> List[BaseTool]:
    manager = MySQLDataBaseManager(connection)
    return [
        ListTablesTool(db_manager=manager),
        TableSchemaTool(db_manager=manager),
        SQLQueryTool(db_manager=manager),
        SQLQueryValidationTool(db_manager=manager),
    ]

tools = get_tools(connection)

system_prompt = """
你是一个专门设计用于与SQL数据库交互的AI智能体。你的任务是将自然语言问题转换为有效的SQL查询语句，以从数据库中检索所需的信息。

给定一个输入问题，你需要按照以下步骤操作:
1.创建一个语法正确的{dialect}查询语句
2.执行查询并查看结果
3.基于查询结果返回最终答案

在生成查询语句时，请遵循以下准则:
除非用户明确指定要获取的具体示例数量，否则始终将查询结果限制为最多{top_k}条。
你可以通过相关列对结果进行排序，以返回数据库中最有意义的示例。
永远不要查询特定表的所有列，只获取与问题相关的列。
在执行查询之前，你必须仔细检查查询语句。如果在执行查询时遇到错误，请重写查询并再次尝试。绝对不要对数据库执行任何数据操作语言(DML)语句(如INSERT、UPDATE、DELETE、DROP等)
开始处理问题时，你应该始终先查看数据库中有哪些表可以查询。不要跳过这一步。
返回的结果应该是名称而不是ID，除非用户明确要求返回ID。你应该尽可能提供有用的上下文信息来支持你的答案，例如相关的表名、列名和查询结果中的关键数据点。
查询用户信息的时候使用用户昵称(nick_name)来作为查询条件，而不是使用用户账号(user_name)。
然后，你应该查看相关表的架构，以了解可用的列和它们的数据类型。
""".format(
    dialect='MySQL',
    top_k=100
)

agent = create_agent(
    llm,
    tools=tools,
    system_prompt=system_prompt
)
