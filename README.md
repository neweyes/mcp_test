# 论坛内容采集框架

> 最后更新时间：2024-03-21

这是一个专门用于论坛内容采集的爬虫框架。本项目专注于高效地爬取多个网站的多个论坛板块，并将内容结构和相关媒体文件以markdown格式保存。

## 主要特性

- **多站点支持**：可同时爬取多个使用不同解析逻辑的网站
- **多板块采集**：支持配置和爬取每个网站内的多个板块
- **内容保存**：
  - 将HTML内容转换为清晰的markdown格式
  - 保持原帖子结构和格式
  - 下载并整理相关媒体文件（图片、视频、音频）
  - 处理多页帖子和回复
- **智能资源管理**：
  - 支持媒体文件断点续传
  - 避免重复下载已有资源
  - 始终刷新帖子内容以获取最新更新
- **反爬虫保护**：
  - 可配置的用户代理（默认使用搜索引擎机器人）
  - 请求间随机延迟
  - 每个板块的并发请求限制
- **进度跟踪**：
  - 整体板块爬取进度
  - 单个帖子爬取状态
  - 媒体下载进度

## 环境要求

- 依赖包：
```
aiohttp # 异步HTTP客户端
aiofiles # 异步文件操作
beautifulsoup4 # HTML解析
markdownify # HTML转Markdown
PyYAML # 配置文件解析
tqdm # 进度条显示
loguru # 日志记录
```

## 安装说明

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

项目使用 `config.yaml` 进行配置：

```yaml
websites:
  - name: "网站A" # 网站标识
    parser: "example_site" # 解析器插件名称
    boards:
      - name: "板块1" # 板块名称
        url: "https://example.com/board1"
        save_dir: "boards/board1" # 内容保存目录
        start_page: 1 # 起始页码
        end_page: 3 # 结束页码
        concurrency: 5 # 每个板块的最大并发请求数
        user_agent: "Googlebot/2.1 (+http://www.google.com/bot.html)"
        delay_range: [1, 3] # 请求间随机延迟（秒）
```

### 输出结构

每个板块的内容按以下结构组织：

```
boards/
  board1/ # 板块保存目录
    markdown/ # 帖子的Markdown文件
      post-title-1.md
      post-title-2.md
    data/ # 下载的媒体文件
      post-title-1/
        image1.jpg
        video1.mp4
      post-title-2/
        image1.jpg
```

### Markdown格式

帖子保存为markdown文件，包含：
- 帖子标题作为标题
- 保持原格式的帖子内容
- 按时间顺序排列的所有回复
- 相对于data目录引用的媒体文件
- 合并多页回复到单个文件

## 项目结构

- `main.py`: 爬虫核心实现
- `parser_plugins/`: 网站特定的解析逻辑
  - `example_site.py`: 示例解析器实现
- `utils/`: 辅助工具
  - `fetcher.py`: 带限速的异步HTTP客户端
  - `markdown_saver.py`: 内容转Markdown转换
  - `parser.py`: 基础解析器接口
  - `sanitize.py`: 文件名清理
- `config.yaml`: 爬虫配置
- `requirements.txt`: 项目依赖

## 添加新网站支持

1. 在 `parser_plugins/` 中创建新的解析器，实现：
  - `get_post_list_urls()`: 从板块页面提取帖子URL
  - `parse_post_detail()`: 从帖子页面提取内容
2. 在 `config.yaml` 中添加网站配置

## 使用方法

运行爬虫：
```bash
python main.py
```

爬虫将：
1. 从 `config.yaml` 加载配置
2. 并行处理每个网站和板块
3. 下载帖子和媒体文件
4. 将内容保存为markdown格式并下载相关媒体

## 开源协议

MIT 开源协议