# Dify Data Visualization Workflow

基于 **Dify 1.15.0 + Docker Compose + Flask + ECharts** 的 Excel/CSV 可视化分析示例。保留原项目的架构：**Dify 代码节点 → Docker 内网 Flask → 保存 HTML → 浏览器查看报表**。

> ⚠️ 此仓库只提供工作流与 Flask 增量部署示例，**不提供、也不需要上传 Dify 的数据库、`.env` 密钥、用户数据、历史 HTML 报告**。请在可信内网测试，未经额外防护不要将 5000 端口直接暴露到公网。生成的 HTML 来自模型输出，打开前应确认内容可信。

## 功能流程

上传 Excel/CSV → Dify 文档提取器 → LLM 生成完整 ECharts HTML → 代码节点提取 HTML → 代码节点 POST 到 `http://dify_flash_server:5000/upload_html` → Flask 保存 → 返回 `/download/report_*.html`。

不上传文件时，工作流走通用问答分支。

## 目录

```text
.
├── README.md
├── Dockerfile.flask
├── html_server.py
├── docker-compose.override.yaml
├── .env.example
├── workflow/
│   └── Excel 数据可视化分析.yml
└── static_files/
    └── .gitkeep
```

## 前提

- 已经部署并正常运行的 **Dify 1.15.0**（其他版本未验证）
- Docker Compose v2；可运行 Linux 容器（Windows 可使用 Docker Desktop + WSL2）
- Dify 内已配置可用的 LLM 模型。原 DSL 使用 **OpenAI API Compatible 插件**，模型名称为 `ark-code-latest`；导入后必须在你自己的 Dify 中重新选择、配置可用模型
- 可以从访问者浏览器打开 Docker 主机的 5000 端口，且必须按实际安全要求限制访问

## 安装：在已有 Dify 上添加 Flask

1. 从此仓库复制 `html_server.py`、`Dockerfile.flask`、`docker-compose.override.yaml` 到 **Dify 官方 `docker/` 文件夹**，在同一目录创建空的 `static_files/`。
2. 在该目录的已有 **`.env`** 中添加一行（保留你原有的全部配置，不要用仓库的示例覆盖）：

   ```dotenv
   REPORT_PUBLIC_BASE_URL=http://YOUR_SERVER_IP:5000
   ```

   把 `YOUR_SERVER_IP` 换成使用者浏览器可以访问的宿主机 IP 或经授权的域名。**不能写 `flask-app` 或 `dify_flash_server`，那是 Docker 内部 DNS 名称。**

3. 在 Dify `docker/` 目录运行：

   ```powershell
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml config --quiet
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml up -d --build flask-app
   ```

   不要用 `docker compose down -v`，否则有删除数据的风险。若你的 compose 项目名不一致，请始终在同一 Dify `docker/` 目录运行命令。

4. 验证 Docker 网络及 Flask 服务（按实际容器名调整）：

   ```powershell
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml ps flask-app
   docker compose -f docker-compose.yaml -f docker-compose.override.yaml exec sandbox sh
   ```

   在 sandbox 中运行 `getent hosts flask-app` 和 `curl http://flask-app:5000/health`。应解析到内网 IP 并得到 `{"status":"ok"}`。

5. 从随附的发布包中取得 `workflow/Excel 数据可视化分析.yml`（此 DSL 文件尚待上传至 GitHub 仓库），然后在 Dify 工作室中**导入 DSL 文件**；确认已安装依赖插件，重新配置两个 LLM 节点，检查“解析链接”代码节点使用 `http://dify_flash_server:5000/upload_html`。**如果你采用本仓库的增量 Compose 而没有设置 `dify_flash_server` 别名，应将此 URL 改成 `http://flask-app:5000/upload_html`。** 上传脱敏测试表格，测试生成的 HTML 链接。

## 故障排查（来自实际部署经历）

| 现象 | 排查方向 |
|---|---|
| `Temporary failure in name resolution` | 代码节点实际运行于 **sandbox**。确认 `flask-app` 与 sandbox 同时加入 `ssrf_proxy_network`，不能只测试 worker。 |
| 手工 `docker network connect` 后能通，重建容器后失败 | 手动连接仅对当前容器有效；请使用本项目 Compose override，永久连接网络。 |
| Flask 返回 URL，但浏览器访问 404 | 原实现与 Flask 内置 `/static` 路由冲突。本项目使用 `static_folder=None` 和 `/download/<filename>`。 |
| Docker 容器能访问，浏览器打不开 | `REPORT_PUBLIC_BASE_URL` 必须是浏览器可访问的宿主机地址；检查 Windows 防火墙、网络策略和映射端口。 |
| 导入后 LLM 节点出错 | 重新安装/配置模型插件，选择本机可调用的模型，导入 DSL 不等于导入模型凭据。 |
| ECharts 空白 | HTML 使用 CDN；浏览器需要能访问 ECharts 资源，或自行改成本地托管资源。 |

## 安全说明

- **不要提交 Dify 原本的 `.env`、数据库备份、`volumes/`、API Key 或业务 Excel。**
- 当前示例上传接口未做认证，报告 URL 也未做登录限制，只适合受信任的内网测试。正式公开使用前请加鉴权、HTTPS、网络访问控制、过期清理，并限制/审查生成的 HTML。
- 本示例保留 Dify 代码节点直接访问同网络 Flask 的工作方式。为保护 Dify sandbox 与 SSRF 边界，请只在受信任环境部署并按照组织安全政策评估网络连通范围。
- 默认生成的文件存放在 `static_files/`，不会被 Git 跟踪。

## 技术说明

Flask 提供 `POST /upload_html`、`GET /download/<filename>`、`GET /health`。工作流 DSL 的解析节点期望 `html_content` 请求字段和 `download_url` JSON 字段。
