# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 MCP (Model Context Protocol) 服务集合仓库，包含多个独立的 Python MCP 服务器实现。每个服务都是独立的 Python 包，使用 FastMCP 框架构建。

## 仓库结构

- `mcp-readonly-mysql/` - 只读 MySQL MCP 服务
- `mcp-elasticsearch/` - Elasticsearch MCP 服务
- 每个服务目录包含：
  - `src/<service_name>/server.py` - 主服务实现
  - `pyproject.toml` - 项目配置和依赖
  - `README.md` - 服务文档
  - `.venv/` - 虚拟环境（已安装）

## 开发命令

### 安装依赖
```bash
cd mcp-<service-name>
uv sync
```

### 运行服务
```bash
cd mcp-<service-name>
uv run mcp-<service-name>
```

### 本地安装（用于 Claude Desktop 配置）
```bash
cd mcp-<service-name>
uv pip install -e .
```

## 架构说明

### FastMCP 框架
所有服务使用 `mcp.server.fastmcp.FastMCP` 框架：
- 使用 `@mcp.tool()` 装饰器定义工具
- 工具函数返回字符串（通常是 JSON 或格式化文本）
- 通过 `mcp.run()` 启动服务

### 配置模式
服务通过环境变量配置，在 Claude Desktop 的 `mcpServers` 配置中通过 `env` 字段传递。


## 添加新服务

1. 创建新目录 `mcp-<service-name>/`
2. 创建 `pyproject.toml`，参考现有服务的结构
3. 在 `src/mcp_<service_name>/server.py` 实现服务
4. 使用 `uv sync` 安装依赖
5. 更新根目录 `README.md`（使用 `/update-readme` skill）
