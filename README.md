# 异步论坛内容采集框架

> 最后更新时间：2024-03-21

这是一个基于Python异步编程的论坛内容采集框架，专注于高效地抓取论坛帖子内容及其相关资源。框架采用插件式设计，支持通过编写解析器插件来扩展对不同论坛的支持。

## 主要特性

- **异步并发处理**：
  - 基于`aiohttp`和`asyncio`的异步请求
  - 可配置的全局并发数限制
  - 内置请求重试机制（最多3次）
  - 可配置的请求间随机延迟

- **智能资源下载**：
  - 支持图片、视频、音频等媒体资源
  - 断点续传功能
  - 自动跳过已下载文件
  - 超时和错误重试处理
  - 分块下载大文件

- **内容处理**：
  - 自动递归获取多页回复
  - 合并主帖和回复内容
  - HTML转Markdown格式
  - 保持原帖子结构
  - 规范化文件命名

- **插件化设计**：
  - 可扩展的网站解析器接口
  - 统一的数据结构规范
  - 示例解析器实现

## 环境要求

- Python 3.7+
- 依赖包：
```
aiohttp     # 异步HTTP客户端
aiofiles    # 异步文件操作
beautifulsoup4  # HTML解析
markdownify  # HTML转Markdown
PyYAML      # 配置文件解析
tqdm        # 进度条显示
loguru      # 日志记录
```

## 安装说明

1. 克隆仓库
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

在`config.yaml`中配置爬取参数：

```yaml
websites:
  - name: "网站A"  # 网站标识
    parser: "example_site"  # 对应parser_plugins目录下的解析器
    boards:
      - name: "板块1"  # 板块名称
        url: "https://example.com/board1"  # 板块URL
        save_dir: "boards/board1"  # 保存目录
        start_page: 1  # 起始页码
        end_page: 3  # 结束页码
concurrency: 5  # 全局最大并发数
user_agent: "Googlebot/2.1"  # 请求头User-Agent
delay_range: [1, 3]  # 请求间随机延迟范围（秒）
```

## 输出结构

```
boards/
  board1/  # 板块目录
    markdown/  # Markdown文件目录
      post-title-1.md  # 帖子内容（包含回复）
      post-title-2.md
    data/  # 媒体文件目录
      post-title-1/  # 按帖子分类
        image1.jpg
        video1.mp4
```

## 项目结构

```
.
├── main.py           # 主程序入口
├── config.yaml       # 配置文件
├── parser_plugins/   # 解析器插件目录
│   ├── __init__.py
│   └── example_site.py  # 示例解析器
├── utils/           # 工具函数
│   ├── fetcher.py      # 异步HTTP请求和文件下载
│   ├── markdown_saver.py  # Markdown格式保存
│   ├── parser.py      # 解析器基类和接口定义
│   └── sanitize.py    # 文件名处理
└── requirements.txt  # 项目依赖
```

## 添加新网站支持

1. 在`parser_plugins/`目录下创建新的解析器模块
2. 实现以下接口：
   ```python
   def get_post_list_urls(board_url, html, start_page, end_page):
       """解析板块页面获取帖子URL列表"""
       return ['帖子URL1', '帖子URL2', ...]

   def parse_post_detail(html):
       """解析帖子详情页面"""
       return {
           'title': '帖子标题',
           'content_markdown': '主帖内容',
           'replies': [{  # 回复列表
               'content_markdown': '回复内容',
               'resources': [{  # 资源文件
                   'url': '文件URL',
                   'filename': '文件名'
               }]
           }],
           'next_reply_page': '下一页URL或None',  # 用于递归获取多页回复
           'resources': [{  # 主帖资源文件
               'url': '文件URL',
               'filename': '文件名'
           }]
       }
   ```

3. 在`config.yaml`中添加新网站配置

## 使用方法

1. 配置`config.yaml`，设置目标网站、板块和并发参数
2. 运行爬虫：
```bash
python main.py
```

程序将：
1. 异步并发处理每个板块
2. 获取帖子列表
3. 递归获取帖子内容和多页回复
4. 下载媒体资源（支持断点续传）
5. 保存为Markdown格式

## 开源协议

MIT