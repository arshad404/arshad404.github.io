import base64
import html
import json
import re
from pathlib import Path


def markdown_to_html(markdown):
    blocks = []
    in_code = False
    code = []
    for line in markdown.splitlines():
        if line.startswith('```'):
            if in_code:
                blocks.append(f'<pre>{html.escape("\n".join(code))}</pre>')
                code = []
            in_code = not in_code
        elif in_code:
            code.append(line)
        elif line.startswith('## '):
            blocks.append(f'<h2>{html.escape(line[3:])}</h2>')
        elif line.startswith('### '):
            blocks.append(f'<h3>{html.escape(line[4:])}</h3>')
        elif line.strip() and not line.startswith('# ') and not re.fullmatch(r'(?:#[a-zA-Z0-9_-]+\s*)+', line.strip()):
            blocks.append(f'<p>{html.escape(line.strip())}</p>')
    return ''.join(blocks)


def parse_post(path):
    markdown = path.read_text(encoding='utf-8')
    front_matter = dict(re.findall(r'^([a-z_]+):\s*(.+)$', markdown, re.MULTILINE)) if markdown.startswith('---\n') else {}
    title_match = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    if not title_match:
        return None
    year = path.parts[1]
    tags = list(dict.fromkeys(re.findall(r'#[a-zA-Z0-9_-]+', markdown.lower())))
    body = re.sub(r'^---\n.*?\n---\n*', '', markdown, count=1, flags=re.DOTALL)
    body = re.sub(r'^#\s+.+$', '', body, count=1, flags=re.MULTILINE)
    plain = re.sub(r'#[a-zA-Z0-9_-]+', '', body)
    plain = re.sub(r'[*_`]', '', plain)
    plain = re.sub(r'\s+', ' ', plain).strip()
    slug = path.stem
    published = front_matter.get('published', f'{year}-01-01T00:00:00Z')
    return {'title': title_match.group(1).strip(), 'year': year, 'published': published, 'source': front_matter.get('source', 'journal'), 'medium_url': front_matter.get('medium_url', ''), 'topic': tags[0][1:] if tags else 'journal', 'tags': tags, 'excerpt': plain[:180] + ('...' if len(plain) > 180 else ''), 'read': f'{max(1, (len(plain.split()) + 199) // 200)} min read', 'html': markdown_to_html(body), 'url': f'year/{year}/{slug}.html'}


posts = [post for path in sorted(Path('year').glob('*/*.md')) if (post := parse_post(path))]
posts.sort(key=lambda post: post['year'], reverse=True)
Path('posts.json').write_text(json.dumps(posts, indent=2) + '\n', encoding='utf-8')

for post in posts:
    destination = Path(post['url'])
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_link = f'<p><span class="source">Imported from Medium</span><span aria-hidden="true"> · </span><a href="{html.escape(post["medium_url"])}" target="_blank" rel="noreferrer">Medium ↗</a></p>' if post['medium_url'] else ''
    destination.write_text(f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="description" content="{html.escape(post['excerpt'])}"><title>{html.escape(post['title'])} - Arshad's Journal</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet"><style>:root{{--ink:#172321;--muted:#68736f;--line:#dfe6e1;--paper:#fbfcfa;--mint:#d9eee4;--coral:#f47e68;--blue:#2f6c72}}*{{box-sizing:border-box}}body{{margin:0;color:var(--ink);background:var(--paper);font:16px/1.7 'Space Grotesk',sans-serif}}main{{width:min(720px,calc(100% - 40px));margin:0 auto;padding:42px 0 90px}}a{{color:var(--blue);text-decoration:none}}.back{{font:500 .76rem 'DM Mono',monospace;color:var(--muted)}}.meta{{display:flex;justify-content:space-between;color:var(--muted);font:500 .74rem 'DM Mono',monospace;text-transform:uppercase;letter-spacing:.08em;margin:80px 0 20px}}h1{{font-size:clamp(2.6rem,7vw,5.2rem);line-height:1;letter-spacing:-.08em;margin:0 0 38px}}article{{color:var(--muted);font-size:1.08rem}}article h2,article h3{{color:var(--ink);margin-top:34px}}article pre{{overflow-x:auto;padding:18px;background:var(--ink);color:#fff}}@media(max-width:600px){{main{{width:min(100% - 28px,560px)}}}}</style></head>
<body><main><a class="back" href="../../index.html">← Back to all writing</a><div class="meta"><span>{post['year']} / {html.escape(post['topic'])}</span><span>{post['read']}</span></div><h1>{html.escape(post['title'])}</h1><p>Published {post['published'].replace('T', ' ').replace('Z', ' UTC')}</p>{source_link}<article>{post['html']}</article></main></body></html>
''', encoding='utf-8')

index = Path('index.html')
source = index.read_text(encoding='utf-8')
payload = base64.b64encode(json.dumps(posts).encode('utf-8')).decode('ascii')
source = re.sub(r'const embeddedPosts = .*?;\n    const grid', f"const embeddedPosts = JSON.parse(atob('{payload}'));\n    const grid", source, count=1, flags=re.DOTALL)
index.write_text(source, encoding='utf-8')