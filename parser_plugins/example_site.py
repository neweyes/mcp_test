from bs4 import BeautifulSoup

def get_post_list_urls(board_url, html, start_page, end_page):
    # TODO: 解析帖子列表页，返回帖子详情页URL列表
    soup = BeautifulSoup(html, 'lxml')
    # 示例：return [a['href'] for a in soup.select('.post-link')]
    return []

def parse_post_detail(html):
    # TODO: 解析帖子详情页，返回内容、资源、回复、下一页回复URL
    soup = BeautifulSoup(html, 'lxml')
    # 示例结构
    return {
        'title': '帖子标题',
        'content_markdown': '正文内容，含图片/视频/音频/链接的markdown格式',
        'resources': [
            # {'url': 'http://...', 'type': 'image', 'filename': 'xxx.jpg'}
        ],
        'replies': [
            # {'content_markdown': '回复内容', 'resources': [...]}
        ],
        'next_reply_page': None
    }
