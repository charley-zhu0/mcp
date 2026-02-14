from mcp.server.fastmcp import FastMCP
import mysql.connector
from mysql.connector import Error
import os
from typing import Optional, List, Dict, Any

# 初始化 FastMCP 服务
mcp = FastMCP("mysql-readonly")

def get_connection():
    """建立 MySQL 数据库连接"""
    try:
        # 优先从环境变量获取，也可以从后续的参数中灵活调整，
        # 但标准 MCP 实践通常通过环境变量配置服务，或者让工具接受参数。
        # 考虑到安全性，数据库凭据最好通过环境变量传递给 MCP 服务器进程。
        host = os.environ.get("MYSQL_HOST", "localhost")
        port = int(os.environ.get("MYSQL_PORT", "3306"))
        user = os.environ.get("MYSQL_USER", "root")
        password = os.environ.get("MYSQL_PASSWORD", "")
        database = os.environ.get("MYSQL_DATABASE", "")

        if not database:
             # 如果没有指定默认数据库，连接时不指定
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
        else:
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )

        if connection.is_connected():
            return connection
    except Error as e:
        raise RuntimeError(f"Failed to connect to MySQL: {e}")
    return None

def is_read_only_query(query: str) -> bool:
    """
    检查 SQL 查询是否为允许的只读操作。
    允许: SELECT, DESCRIBE, DESC, SHOW, EXPLAIN
    """
    query = query.strip().upper()
    allowed_prefixes = ("SELECT", "DESCRIBE", "DESC", "SHOW", "EXPLAIN")
    return query.startswith(allowed_prefixes)

@mcp.tool()
def list_databases() -> str:
    """列出所有可用的数据库"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        return "\n".join(databases)
    except Error as e:
        return f"Error: {e}"
    finally:
        if conn and conn.is_connected():
            conn.close()

@mcp.tool()
def list_tables(database: str) -> str:
    """列出指定数据库中的所有表"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # 切换数据库
        cursor.execute(f"USE {database}")
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        return "\n".join(tables)
    except Error as e:
        return f"Error: {e}"
    finally:
        if conn and conn.is_connected():
            conn.close()

@mcp.tool()
def describe_table(database: str, table_name: str) -> str:
    """获取表结构信息 (DESCRIBE table)"""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"USE {database}")
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()

        # 格式化输出
        result = [f"Table: {table_name}"]
        for col in columns:
            field = col.get('Field', 'N/A')
            type_ = col.get('Type', 'N/A')
            null = col.get('Null', 'N/A')
            key = col.get('Key', '')
            default = col.get('Default', 'NULL')
            extra = col.get('Extra', '')
            result.append(f"- {field} ({type_}) {'[PK]' if key == 'PRI' else ''} Null:{null} Default:{default} {extra}")

        return "\n".join(result)
    except Error as e:
        return f"Error: {e}"
    finally:
        if conn and conn.is_connected():
            conn.close()

@mcp.tool()
def run_read_only_sql(database: str, query: str) -> str:
    """
    执行只读 SQL 查询 (SELECT, SHOW, EXPLAIN, DESCRIBE)。
    禁止执行 INSERT, UPDATE, DELETE, DROP 等修改操作。
    """
    if not is_read_only_query(query):
        return "Error: Only read-only queries (SELECT, SHOW, DESCRIBE, EXPLAIN) are allowed."

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"USE {database}")
        cursor.execute(query)

        rows = cursor.fetchall()
        if not rows:
            return "No results found."

        return str(rows)
    except Error as e:
        return f"Error executing query: {e}"
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    mcp.run()
