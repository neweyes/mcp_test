from parser_plugins import example_site

def test_get_post_list_urls():
    html = '<html></html>'
    urls = example_site.get_post_list_urls('http://test', html, 1, 1)
    assert isinstance(urls, list)

def test_parse_post_detail():
    html = '<html></html>'
    detail = example_site.parse_post_detail(html)
    assert 'title' in detail
    assert 'content_markdown' in detail
    assert 'resources' in detail
    assert 'replies' in detail
