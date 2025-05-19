import os
from .sanitize import sanitize_filename

def save_post_as_markdown(post, save_dir, data_dir):
    title = sanitize_filename(post['title'])
    md_dir = os.path.join(save_dir, "markdown")
    data_post_dir = os.path.join(data_dir, title)
    os.makedirs(md_dir, exist_ok=True)
    os.makedirs(data_post_dir, exist_ok=True)
    md_path = os.path.join(md_dir, f"{title}.md")
    content = post['content_markdown']
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {post['title']}\n\n{content}")
    return data_post_dir
