# Crawl Sitepage

## 项目简介

本项目是一个可扩展的多站点多板块爬虫，支持抓取指定网站的帖子内容（含多页回复），将帖子内容、图片、视频、音频、链接等保存为本地markdown文档和资源文件夹。支持多板块、并发配置、UA伪装、断点下载、插件式解析。

## 目录结构

```
crawl-sitepage/
├── main.py                # 主程序入口
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖列表
├── README.md              # 项目说明
├── tests/                 # 测试用例
├── parser_plugins/        # 各网站解析插件
│   ├── __init__.py
│   └── example_site.py    # 示例解析器
└── utils/
    ├── fetcher.py
    ├── markdown_saver.py
    └── sanitize.py
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

编辑 `config.yaml`，示例：

```yaml
websites:
  - name: "网站A"
    parser: "example_site"
    boards:
      - name: "板块1"
        url: "https://example.com/board1"
        save_dir: "boards/board1"
        start_page: 1
        end_page: 3
      - name: "板块2"
        url: "https://example.com/board2"
        save_dir: "boards/board2"
        start_page: 1
        end_page: 2
concurrency: 5
user_agent: "Googlebot/2.1 (+http://www.google.com/bot.html)"
delay_range: [1, 3]
```

- `parser` 字段指定解析插件（位于 parser_plugins/ 下）。
- `start_page`/`end_page` 支持指定抓取的起止页。

## 运行

```bash
python main.py
```

## 扩展新网站
1. 在 `parser_plugins/` 下新建 `your_site.py`，实现 `get_post_list_urls` 和 `parse_post_detail` 两个函数。
2. 在 `config.yaml` 的 `parser` 字段指定为你的插件名。

## 测试

见 `tests/` 目录，运行：
```bash
pytest tests/
```

## 断点续传说明
- 资源（图片/视频/音频）下载采用断点续传，已存在则跳过。
- markdown内容每次都重新抓取。

## 其他
- 支持多板块、分目录保存、并发可调、UA伪装。
- markdown内容和资源分开存储，markdown在 markdown 目录下，资源在 data 目录下。
