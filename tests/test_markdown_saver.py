import os
from utils.markdown_saver import save_post_as_markdown

def test_save_post_as_markdown(tmp_path):
    post = {
        'title': '测试标题',
        'content_markdown': '正文内容',
        'resources': []
    }
    save_dir = tmp_path
    data_dir = os.path.join(save_dir, 'data')
    post_dir = save_post_as_markdown(post, save_dir, data_dir)
    md_path = os.path.join(save_dir, 'markdown', '测试标题.md')
    assert os.path.exists(md_path)
    with open(md_path, encoding='utf-8') as f:
        assert '正文内容' in f.read()
