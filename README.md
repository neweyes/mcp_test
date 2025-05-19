# 论坛内容采集框架

> 最后更新时间：2024-03-21

这是一个基于Python异步编程的论坛内容采集框架，专注于高效地抓取论坛帖子内容及其相关资源。

## 主要特性

- **异步并发抓取**：
  - 使用`aiohttp`实现异步HTTP请求
  - 可配置的全局并发数限制
  - 支持请求间随机延迟
- **多页内容处理**：
  - 自动处理分页帖子内容
  - 递归获取所有回复页面
  - 合并为单一完整内容
- **资源文件处理**：
  - 自动下载帖子中的媒体资源（图片/视频/音频）
  - 支持断点续传
  - 避免重复下载
- **内容格式化**：
  - HTML转Markdown格式
  - 保持原帖子结构
  - 规范化文件命名
- **可扩展解析器**：
  - 插件式网站解析器
  - 统一的解析器接口
  - 易于添加新网站支持

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
      post-title-1.md
      post-title-2.md
    data/  # 媒体文件目录
      post-title-1/
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
│   ├── fetcher.py      # 异步HTTP请求
│   ├── markdown_saver.py  # Markdown保存
│   ├── parser.py      # 解析器基类
│   └── sanitize.py    # 文件名处理
└── requirements.txt  # 项目依赖
```

## 添加新网站支持

1. 在`parser_plugins/`目录下创建新的解析器模块
2. 实现以下接口：
   - `get_post_list_urls(board_url, html, start_page, end_page)`: 解析板块页面获取帖子URL列表
   - `parse_post_detail(html)`: 解析帖子详情页面，返回包含以下字段的字典：
     ```python
     {
         'title': '帖子标题',
         'content_markdown': '主帖内容',
         'replies': [{  # 回复列表
             'content_markdown': '回复内容',
             'resources': [{  # 资源文件
                 'url': '文件URL',
                 'filename': '文件名'
             }]
         }],
         'next_reply_page': '下一页URL',  # 如果有分页
         'resources': [{  # 主帖资源文件
             'url': '文件URL',
             'filename': '文件名'
         }]
     }
     ```
3. 在`config.yaml`中添加新网站配置

## 使用方法

1. 配置`config.yaml`
2. 运行爬虫：
```bash
python main.py
```

程序将：
1. 异步并发处理每个板块
2. 获取帖子列表和详情
3. 递归获取多页回复
4. 下载媒体资源
5. 保存为Markdown格式

## 开源协议

MIT