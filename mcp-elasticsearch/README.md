# Elasticsearch MCP Server

这是一个 Elasticsearch Model Context Protocol (MCP) 服务。它允许 LLM 与 Elasticsearch 集群交互，执行搜索、索引管理和文档操作。

## 功能

### 集群信息
*   `es_cluster_health`: 获取集群健康状态
*   `es_list_indices`: 列出所有索引
*   `es_get_mapping`: 获取索引的映射结构

### 读取操作
*   `es_search`: 搜索文档（支持 Elasticsearch Query DSL）
*   `es_get_document`: 根据 ID 获取文档
*   `es_count`: 统计文档数量

### 写入操作
*   `es_index_document`: 索引文档（创建或更新）
*   `es_update_document`: 更新现有文档
*   `es_delete_document`: 删除文档

### 索引管理
*   `es_create_index`: 创建索引（支持自定义映射）
*   `es_delete_index`: 删除索引

## 前置要求

*   [uv](https://github.com/astral-sh/uv) (推荐用于管理 Python 环境和运行工具)
*   一个 Elasticsearch 集群实例

## 配置与使用

此服务使用环境变量来配置 Elasticsearch 连接。

### 环境变量

*   `ES_SCHEME`: 连接协议 (默认: http，可选: https)
*   `ES_HOST`: Elasticsearch 地址 (默认: localhost)
*   `ES_PORT`: 端口 (默认: 9200)
*   `ES_USER`: 用户名（可选）
*   `ES_PASSWORD`: 密码（可选）

### 在 Claude Desktop 中添加

将以下配置添加到你的 Claude Desktop 配置文件中：

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

**注意**: 请将 `/path/to/your/mcp-elasticsearch` 替换为你实际存放此项目的绝对路径。

### 本地测试

```bash
# 在项目根目录下
export ES_HOST=localhost
export ES_PORT=9200
export ES_USER=elastic
export ES_PASSWORD=your_password
uv run src/mcp_elasticsearch/server.py
```

## 使用示例

### 搜索文档
```python
# query 参数使用 Elasticsearch Query DSL
es_search(
    index="my_index",
    query='{"match": {"title": "search term"}}',
    size=10
)
```

### 索引文档
```python
es_index_document(
    index="my_index",
    document='{"title": "My Document", "content": "Document content"}',
    doc_id="doc_1"  # 可选
)
```

### 创建索引
```python
es_create_index(
    index="my_index",
    mappings='{"properties": {"title": {"type": "text"}, "date": {"type": "date"}}}'
)
```
