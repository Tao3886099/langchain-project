from typing import List

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from agent.utils.log_utils import log


class MySQLDataBaseManager:
    """MySQL数据库管理器，提供连接和执行SQL语句的功能"""

    def __init__(self, connection: str):
        """初始化数据库管理器

        Args:
            connection: 数据库连接字符串，格式为 "mysql+pymysql://user:password@host:port/database"
        """
        self.connection = connection
        # 这里可以添加实际的数据库连接逻辑，例如使用 SQLAlchemy 创建引擎等
        self.engine = create_engine(connection, pool_recycle=3600, pool_size=5, max_overflow=10)

    def get_table_names(self) -> list[str]:
        """获取数据库中的表名列表"""
        try:
            # 创建一个数据库映射对象获取数据库中的表名
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表名时发生错误: {str(e)}")


    def get_table_comments(self) -> List[dict]:
        """
        获取数据库中所有表的名称和注释信息

        Returns:
            List[dict]: 包含表名称和注释信息的字典列表，每个字典包含 'table_name' 和 'comment' 键
        """
        try:
            # 构建查询语句获取表名称和注释信息
            query = text("""
                        SELECT table_name, table_comment
                        FROM information_schema.tables
                        WHERE table_schema = DATABASE()
                            AND table_type = 'BASE TABLE'
                        Order by table_name
            """)

            with self.engine.connect() as connection:
                result = connection.execute(query)
                table_comments = [{ "table_name": row[0],"comment": row[1]} for row in result]
                return table_comments
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表注释时发生错误: {str(e)}")

    def get_table_schema(self, table_name: str) -> List[dict]:
        """获取指定表的字段信息，包括字段名称、数据类型、是否可为空等

        Args:
            table_name: 表名

        Returns:
            包含字段信息的字典列表，每个字典包含 'column_name', 'data_type', 'is_nullable' 等键
        """
        try:
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            return columns
        except SQLAlchemyError as e:
            log.exception(e)
            raise ValueError(f"获取表结构时发生错误: {str(e)}")



if __name__ == "__main__":
    # 示例用法

    # 配置数据库连接信息
    DB_CONFIG = {
        "host": "139.159.228.234",
        "port": 3306,
        "user": "root",
        "password": "Tao3886099",
        "database": "ry-vue"
    }
    connection = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"
    db_manager = MySQLDataBaseManager(connection)
    table_names = db_manager.get_table_names()
    print(table_names)

    table_comments = db_manager.get_table_comments()
    print(table_comments)

    table_colums = db_manager.get_table_schema("sys_user")
    print(table_colums)