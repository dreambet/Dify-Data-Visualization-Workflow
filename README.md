<div align="center">

# 📊 Dify Data Visualization Workflow

### 基于 Dify 的智能数据分析与可视化工作流

**从 Excel / CSV 数据输入，到 AI 分析、ECharts 看板生成与 HTML 报表发布的一体化方案。**

<p>
  <img src="https://img.shields.io/badge/Dify-1.15.0-2563EB?style=flat-square" alt="Dify 1.15.0">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Flask-HTML_Service-16A34A?style=flat-square" alt="Flask">
  <img src="https://img.shields.io/badge/ECharts-Visualization-AA344D?style=flat-square" alt="ECharts">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-64748B?style=flat-square" alt="MIT License"></a>
</p>

[功能概览](#features) · [系统架构](#architecture) · [快速开始](#quick-start) · [故障排查](#troubleshooting)

</div>

---

## 📌 关于项目

**Dify Data Visualization Workflow** 是一个基于 **Dify Chatflow + Docker + Flask + ECharts** 构建的数据分析可视化解决方案。

项目解决企业数据分析场景中“上传业务数据 → AI 自动分析 → 生成可交互图表 → 输出 HTML 看板”的完整链路问题。

核心设计理念：

> 利用 Dify 负责 AI 工作流编排，利用 Flask 负责 HTML 文件生成与访问，实现低代码的数据分析可视化应用。

| 使用场景 | 支持能力 |
| :--- | :--- |
| 数据分析 | 上传 Excel / CSV，自动提取数据特征并生成分析结果 |
| AI 辅助 | 使用大模型生成分析逻辑、指标解释和可视化方案 |
| 图表展示 | 自动生成 ECharts HTML 交互式数据看板 |
| 企业部署 | 支持本地服务器 Docker 化部署，数据不离开内部环境 |

<a id="features"></a>

## ✨ 功能概览

### 🤖 AI 数据分析流程

| 功能 | 说明 |
| :--- | :--- |
| 文件上传 | 支持 Excel / CSV 数据输入 |
| 数据解析 | Dify 文档节点读取业务数据 |
| 智能分析 | LLM 自动生成指标分析和可视化方案 |
| 看板生成 | 输出完整 ECharts HTML 页面 |
| 报表访问 | Flask 保存并提供浏览器访问链接 |

### 🖥️ HTML 看板服务

| 功能 | 说明 |
| :--- | :--- |
| Flask API | 接收 Dify 生成的 HTML 内容 |
| 文件管理 | 自动生成唯一报告文件 |
| Docker 集成 | 与 Dify Sandbox 内网通信 |
| 浏览访问 | 返回可直接打开的数据看板地址 |

<a id="architecture"></a>

## 🏗️ 系统架构

```text
用户
 │
 ▼
Dify Chatflow
 │
 ├── 文件上传
 │
 ├── 数据解析
 │
 ├── LLM 数据分析
 │
 ├── 生成 ECharts HTML
 │
 ▼
Dify Sandbox
 │
 │ Docker 内网
 ▼
Flask HTML Service
 │
 ├── 保存 HTML 文件
 │
 └── 返回访问 URL
 │
 ▼
浏览器查看数据看板
```

### 技术组成

| 模块 | 技术 |
| :--- | :--- |
| AI 工作流 | Dify Chatflow |
| 数据处理 | Dify Workflow Node |
| 大模型 | OpenAI Compatible Model / 企业模型 |
| 可视化 | Apache ECharts |
| 服务端 | Python Flask |
| 部署 | Docker Compose |
| 文件存储 | Local Volume |

---

## 📁 项目结构

```text
Dify-Data-Visualization-Workflow/
│
├── README.md
├── Dockerfile.flask                 # Flask 服务镜像
├── html_server.py                   # HTML 文件生成服务
├── docker-compose.override.yaml     # Dify 增量部署配置
├── .env.example                     # 环境变量示例
│
├── workflow/
│   └── Excel 数据可视化分析.yml     # Dify Chatflow DSL
│
└── static_files/
    └── .gitkeep                     # HTML 存储目录
```

<a id="quick-start"></a>

## 🚀 快速开始

### 环境要求

- 已部署运行的 Dify（推荐 1.15.0）
- Docker Compose v2
- 可调用的大模型配置
- 浏览器可以访问服务器 5000 端口

---

### 1. 部署 Flask 服务

复制以下文件至 Dify 官方 `docker/` 目录：

```text
html_server.py
Dockerfile.flask
docker-compose.override.yaml
```

创建目录：

```text
static_files/
```

启动：

```powershell
docker compose -f docker-compose.yaml -f docker-compose.override.yaml up -d --build
```

---

### 2. 配置访问地址

在 Dify `.env` 增加：

```dotenv
REPORT_PUBLIC_BASE_URL=http://YOUR_SERVER_IP:5000
```

注意：

- `flask-app` 是 Docker 内部访问名称
- `YOUR_SERVER_IP` 是用户浏览器访问地址

两者用途不同。

---

### 3. 导入 Dify Workflow

进入：

```text
Dify Studio
 → 工作室
 → 导入 DSL
```

选择：

```text
workflow/Excel 数据可视化分析.yml
```

导入后重新配置模型节点即可运行。

---

## 🔄 数据处理流程

```text
Excel / CSV
    ↓
Dify 文件解析
    ↓
LLM 数据分析
    ↓
生成 ECharts HTML
    ↓
Flask 保存 HTML
    ↓
返回访问链接
    ↓
浏览器查看 Dashboard
```

<a id="troubleshooting"></a>

## 🛠️ 常见问题

| 问题 | 解决方案 |
| :--- | :--- |
| Temporary failure in name resolution | 检查 Flask 与 Dify Sandbox 是否加入同一 Docker 网络 |
| Docker 能访问，浏览器打不开 | 检查 `REPORT_PUBLIC_BASE_URL` 是否填写服务器 IP |
| HTML 返回 404 | 使用 `/download/` 路由，不使用 Flask 默认 static 路由 |
| Workflow 导入后模型报错 | 重新绑定本地可用模型 |
| ECharts 页面空白 | 检查浏览器是否可以访问 ECharts CDN |

---

## 🔐 安全说明

- 不上传 Dify `.env`、数据库、API Key、业务 Excel 文件。
- 本项目提供的是 Dify 扩展组件，不包含完整 Dify 平台。
- Flask 上传接口默认适用于内网环境，公网部署请增加鉴权。
- 生产环境建议增加 HTTPS、访问控制和文件清理策略。

---

## 📄 License

MIT License
