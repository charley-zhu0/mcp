# MCP Services

本仓库包含以下 MCP (Model Context Protocol) 服务：

## 目录

- [mcp-readonly-mysql](#mcp-readonly-mysql)
- [mcp-elasticsearch](#mcp-elasticsearch)

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

## mcp-elasticsearch

**简介**: Elasticsearch Model Context Protocol (MCP) 服务，允许 LLM 与 Elasticsearch 集群交互，执行搜索、索引管理和文档操作。

### 提供的工具

| 工具名 | 描述 |
|--------|------|
| `es_cluster_health` | 获取集群健康状态 |
| `es_list_indices` | 列出所有索引 |
| `es_get_mapping` | 获取索引的映射结构 |
| `es_search` | 搜索文档（支持 Elasticsearch Query DSL） |
| `es_get_document` | 根据 ID 获取文档 |
| `es_count` | 统计文档数量 |
| `es_index_document` | 索引文档（创建或更新） |
| `es_update_document` | 更新现有文档 |
| `es_delete_document` | 删除文档 |
| `es_create_index` | 创建索引（支持自定义映射） |
| `es_delete_index` | 删除索引 |

### 配置参数

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `ES_SCHEME` | 连接协议 (http/https) | `http` |
| `ES_HOST` | Elasticsearch 地址 | `localhost` |
| `ES_PORT` | 端口 | `9200` |
| `ES_USER` | 用户名 | `""` |
| `ES_PASSWORD` | 密码 | `""` |

### Claude Desktop 配置

```json
{
  "mcpServers": {
    "elasticsearch": {
      "command": "uvx",
      "args": [
        "--from",
        "/path/to/your/mcp-elasticsearch",
        "mcp-elasticsearch"
      ],
      "env": {
        "ES_SCHEME": "http",
        "ES_HOST": "localhost",
        "ES_PORT": "9200",
        "ES_USER": "your_username",
        "ES_PASSWORD": "your_password"
      }
    }
  }
}
```

---
