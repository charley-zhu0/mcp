# MCP Services

本仓库包含以下 MCP (Model Context Protocol) 服务：

## 目录

- [mcp-readonly-mysql](#mcp-readonly-mysql)

---

## mcp-readonly-mysql

**简介**: 这是一个只读的 MySQL Model Context Protocol (MCP) 服务。它允许 LLM 安全地检查数据库结构和查询数据，但阻止任何修改操作。

### 提供的工具

| 工具名 | 描述 |
|--------|------|
| `list_databases` | 列出所有可用的数据库 |
| `list_tables` | 列出指定数据库中的所有表 |
| `describe_table` | 获取表结构信息 (DESCRIBE table) |
| `run_read_only_sql` | 执行只读 SQL 查询 (SELECT, SHOW, EXPLAIN, DESCRIBE)。禁止执行 INSERT, UPDATE, DELETE, DROP 等修改操作。 |

### 配置参数

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `MYSQL_HOST` | 数据库地址 | `localhost` |
| `MYSQL_PORT` | 端口 | `3306` |
| `MYSQL_USER` | 用户名 | `root` |
| `MYSQL_PASSWORD` | 密码 | `""` |
| `MYSQL_DATABASE` | 默认数据库 | `""` |

### Claude Desktop 配置

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

---
