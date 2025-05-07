import asyncio
import yaml
import aiohttp
import os
import importlib
from utils.fetcher import fetch, download_file
from utils.markdown_saver import save_post_as_markdown
from utils.sanitize import sanitize_filename
from loguru import logger
from tqdm import tqdm

# 每个板块独立并发
async def crawl_board(board, parser, config, website_name):
    headers = {'User-Agent': config['user_agent']}
    sem = asyncio.Semaphore(config['concurrency'])
    async with aiohttp.ClientSession() as session:
        post_urls = []
        for page in range(board.get('start_page', 1), board.get('end_page', 1) + 1):
            page_url = f"{board['url']}?page={page}"
            html = await fetch(session, page_url, headers, sem, config['delay_range'])
            post_urls += parser.get_post_list_urls(board['url'], html, board.get('start_page', 1), board.get('end_page', 1))
        with tqdm(total=len(post_urls), desc=f"{website_name}-{board['name']} 总进度") as pbar_board:
            tasks = [crawl_post(post_url, board['save_dir'], session, headers, sem, config, parser, pbar_board) for post_url in post_urls]
            await asyncio.gather(*tasks)

async def crawl_post(post_url, save_dir, session, headers, sem, config, parser, pbar_board):
    replies = []
    next_url = post_url
    post_data = None
    # 递归抓取多页回复
    with tqdm(total=1, desc=f"抓取帖子:{post_url[:30]}", leave=False) as pbar_post:
        while next_url:
            html = await fetch(session, next_url, headers, sem, config['delay_range'])
            detail = parser.parse_post_detail(html)
            if not post_data:
                post_data = detail
            replies.extend(detail.get('replies', []))
            next_url = detail.get('next_reply_page')
            pbar_post.update(1)
    post_data['replies'] = replies

    # 合并主内容和所有回复为markdown
    all_md = [post_data['content_markdown']]
    all_resources = post_data.get('resources', [])
    for reply in replies:
        all_md.append('\n---\n' + reply['content_markdown'])
        all_resources.extend(reply.get('resources', []))
    post_data['content_markdown'] = '\n'.join(all_md)
    post_data['resources'] = all_resources

    data_post_dir = save_post_as_markdown(post_data, save_dir, os.path.join(save_dir, "data"))
    # 下载资源（图片/视频/音频），断点下载
    resources = post_data.get('resources', [])
    with tqdm(total=len(resources), desc=f"下载资源:{post_data['title'][:20]}", leave=False) as pbar_res:
        tasks = []
        for res in resources:
            res_path = os.path.join(data_post_dir, res['filename'])
            if not os.path.exists(res_path):
                tasks.append(download_file(session, res['url'], res_path, headers, sem, config['delay_range']))
            pbar_res.update(1)
        if tasks:
            await asyncio.gather(*tasks)
    pbar_board.update(1)

async def crawl_website(website, config):
    parser = importlib.import_module(f'parser_plugins.{website["parser"]}')
    board_tasks = [crawl_board(board, parser, config, website['name']) for board in website['boards']]
    await asyncio.gather(*board_tasks)

async def main():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    website_tasks = [crawl_website(website, config) for website in config['websites']]
    await asyncio.gather(*website_tasks)

if __name__ == '__main__':
    asyncio.run(main())
