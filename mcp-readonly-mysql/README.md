# MySQL Read-Only MCP Server

这是一个只读的 MySQL Model Context Protocol (MCP) 服务。它允许 LLM 安全地检查数据库结构和查询数据，但阻止任何修改操作。

## 功能

*   `list_databases`: 列出所有数据库。
*   `list_tables`: 列出指定数据库中的表。
*   `describe_table`: 查看表结构 (字段、类型、主键等)。
*   `run_read_only_sql`: 执行自定义 SQL 查询。
    *   **安全限制**: 代码层仅允许以 `SELECT`, `DESCRIBE`, `DESC`, `SHOW`, `EXPLAIN` 开头的语句。

## 前置要求

*   [uv](https://github.com/astral-sh/uv) (推荐用于管理 Python 环境和运行工具)
*   一个 MySQL 数据库实例

## 安全建议 (重要)

虽然此 MCP 服务在代码层面拦截了非只读查询，但**强烈建议**在数据库层面创建一个仅拥有 `SELECT` 权限的专用只读用户。

```sql
-- MySQL 示例：创建只读用户
CREATE USER 'mcp_reader'@'%' IDENTIFIED BY 'your_secure_password';
GRANT SELECT, SHOW VIEW ON *.* TO 'mcp_reader'@'%';
FLUSH PRIVILEGES;
```

## 配置与使用

此服务使用环境变量来配置数据库连接。

### 环境变量

*   `MYSQL_HOST`: 数据库地址 (默认: localhost)
*   `MYSQL_PORT`: 端口 (默认: 3306)
*   `MYSQL_USER`: 用户名 (默认: root)
*   `MYSQL_PASSWORD`: 密码
*   `MYSQL_DATABASE`: (可选) 默认数据库

### 在 Claude Desktop 中添加

将以下配置添加到你的 Claude Desktop 配置文件中 (通常位于 `~/Library/Application Support/Claude/claude_desktop_config.json` 或 `%APPDATA%\Claude\claude_desktop_config.json`)：

```json
{
  "mcpServers": {
    "mysql-readonly": {
      "command": "uvx",
      "args": [
        "--from",
        "/path/to/your/mcp-readonly-mysql",
        "mcp-readonly-mysql"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "mcp_reader",
        "MYSQL_PASSWORD": "your_secure_password",
        "MYSQL_DATABASE": "your_database_name"
      }
    }
  }
}
```

**注意**: 请将 `/path/to/your/mcp-readonly-mysql` 替换为你实际存放此项目的绝对路径。

### 本地测试

你可以使用 `mcp-cli` 或直接运行来进行测试（虽然它主要是为 MCP 客户端设计的）：

```bash
# 在项目根目录下
export MYSQL_USER=root
export MYSQL_PASSWORD=secret
uv run src/mcp_readonly_mysql/server.py
```
