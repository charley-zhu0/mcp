from mcp.server.fastmcp import FastMCP
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError, RequestError
import os
import json
from typing import Optional, Dict, Any

mcp = FastMCP("elasticsearch_mcp")

def get_client():
    """创建 Elasticsearch 客户端连接"""
    scheme = os.environ.get("ES_SCHEME", "http")
    host = os.environ.get("ES_HOST", "localhost")
    port = int(os.environ.get("ES_PORT", "9200"))
    user = os.environ.get("ES_USER", "")
    password = os.environ.get("ES_PASSWORD", "")

    if user and password:
        return Elasticsearch(
            [f"{scheme}://{host}:{port}"],
            basic_auth=(user, password)
        )
    return Elasticsearch([f"{scheme}://{host}:{port}"])

@mcp.tool()
def es_cluster_health() -> str:
    """获取集群健康状态"""
    try:
        client = get_client()
        health = client.cluster.health()
        return json.dumps(health.body, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_list_indices() -> str:
    """列出所有索引"""
    try:
        client = get_client()
        indices = client.cat.indices(format="json")
        return json.dumps(indices.body, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_get_mapping(index: str) -> str:
    """获取索引的映射结构"""
    try:
        client = get_client()
        mapping = client.indices.get_mapping(index=index)
        return json.dumps(mapping.body, indent=2)
    except NotFoundError:
        return f"Error: Index '{index}' not found"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_search(index: str, query: str, size: Optional[int] = 10) -> str:
    """搜索文档。query 参数应为 JSON 格式的查询 DSL"""
    try:
        client = get_client()
        query_dict = json.loads(query)
        result = client.search(index=index, query=query_dict, size=size)
        return json.dumps(result.body, indent=2)
    except json.JSONDecodeError:
        return "Error: Invalid JSON query"
    except NotFoundError:
        return f"Error: Index '{index}' not found"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_get_document(index: str, doc_id: str) -> str:
    """根据 ID 获取文档"""
    try:
        client = get_client()
        doc = client.get(index=index, id=doc_id)
        return json.dumps(doc.body, indent=2)
    except NotFoundError:
        return f"Error: Document '{doc_id}' not found in index '{index}'"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_index_document(index: str, document: str, doc_id: Optional[str] = None) -> str:
    """索引文档。document 参数应为 JSON 格式"""
    try:
        client = get_client()
        doc_dict = json.loads(document)
        if doc_id:
            result = client.index(index=index, id=doc_id, document=doc_dict)
        else:
            result = client.index(index=index, document=doc_dict)
        return json.dumps(result.body, indent=2)
    except json.JSONDecodeError:
        return "Error: Invalid JSON document"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_update_document(index: str, doc_id: str, document: str) -> str:
    """更新文档。document 参数应为 JSON 格式"""
    try:
        client = get_client()
        doc_dict = json.loads(document)
        result = client.update(index=index, id=doc_id, doc=doc_dict)
        return json.dumps(result.body, indent=2)
    except json.JSONDecodeError:
        return "Error: Invalid JSON document"
    except NotFoundError:
        return f"Error: Document '{doc_id}' not found in index '{index}'"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_delete_document(index: str, doc_id: str) -> str:
    """删除文档"""
    try:
        client = get_client()
        result = client.delete(index=index, id=doc_id)
        return json.dumps(result.body, indent=2)
    except NotFoundError:
        return f"Error: Document '{doc_id}' not found in index '{index}'"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_create_index(index: str, mappings: Optional[str] = None) -> str:
    """创建索引。mappings 参数为可选的 JSON 格式映射定义"""
    try:
        client = get_client()
        body = {}
        if mappings:
            body["mappings"] = json.loads(mappings)
        result = client.indices.create(index=index, body=body if body else None)
        return json.dumps(result.body, indent=2)
    except json.JSONDecodeError:
        return "Error: Invalid JSON mappings"
    except RequestError as e:
        return f"Error: {e.info}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_delete_index(index: str) -> str:
    """删除索引"""
    try:
        client = get_client()
        result = client.indices.delete(index=index)
        return json.dumps(result.body, indent=2)
    except NotFoundError:
        return f"Error: Index '{index}' not found"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def es_count(index: str, query: Optional[str] = None) -> str:
    """统计文档数量。query 参数为可选的 JSON 格式查询 DSL"""
    try:
        client = get_client()
        if query:
            query_dict = json.loads(query)
            result = client.count(index=index, query=query_dict)
        else:
            result = client.count(index=index)
        return json.dumps(result.body, indent=2)
    except json.JSONDecodeError:
        return "Error: Invalid JSON query"
    except NotFoundError:
        return f"Error: Index '{index}' not found"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
