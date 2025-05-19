import re

def sanitize_filename(name: str) -> str:
    # 替换非法字符为下划线
    return re.sub(r'[\\/:*?"<>|]', '_', name)
