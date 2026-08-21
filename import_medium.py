import html
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class MediumBodyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines = []
        self.current = []
        self.in_pre = False
        self.list_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.flush()
            self.in_pre = True
            self.current.append('```\n')
        elif tag in {'h2', 'h3', 'h4'}:
            self.flush()
            self.current.append(f"{'#' * (int(tag[1]) - 1)} ")
        elif tag == 'li':
            self.flush()
            self.current.append('- ')
        elif tag == 'br' and self.in_pre:
            self.current.append('\n')

    def handle_endtag(self, tag):
        if tag == 'pre':
            self.current.append('\n```')
            self.flush()
            self.in_pre = False
        elif tag in {'p', 'h2', 'h3', 'h4', 'li'}:
            self.flush()

    def handle_data(self, data):
        self.current.append(data)

    def flush(self):
        text = ''.join(self.current).strip()
        if text:
            self.lines.append(re.sub(r'\s+', ' ', text) if not self.in_pre else text)
        self.current = []


def body_to_markdown(content):
    parser = MediumBodyParser()
    parser.feed(content)
    parser.flush()
    return '\n\n'.join(parser.lines)


def slug_for(item):
    path = urlparse(item.findtext('link', '')).path.strip('/').split('/')[-1]
    return re.sub(r'[^a-z0-9]+', '-', path.lower()).strip('-') or 'medium-post'


TITLE_OVERRIDES = {
    'agentic-ai-what-is-context-and-semantics-in-vector-9c049b901e98': 'Understanding Context and Semantics in Vector Databases',
    'arraydeque-vs-stack-in-java-which-one-to-use-c1eaa23cc7a9': 'ArrayDeque vs Stack in Java: Choosing the Right Tool',
    'is-java-vector-different-than-arraylist-40bd3765035d': 'Java Vector vs ArrayList: Thread Safety and Performance',
    'jdbc-jpa-internals-2-replacing-jpa-with-raw-jdbc-in-a-spring-boot-application-602cdf3a9e4c': 'Replacing JPA with JDBC in Spring Boot',
    'jdbc-jpa-internals-3-connection-pool-benchmark-test-coding-b71788861fa5': 'JDBC Connection Pools in Spring Boot: 3206ms to 372ms',
    'nested-loop-hash-and-merge-join-usage-during-optimiser-phase-for-parse-tree-benchmarking-a5a04b782d9c': 'Comparing SQL Join Strategies: Nested Loop, Hash Join, and Merge Join',
    'netflix-made-its-databases-75-faster-by-moving-from-self-managed-postgres-on-ec2-to-amazon-aurora-58470ccccb4f': 'How Netflix Improved Database Performance with Amazon Aurora',
    'understanding-java-arraylist-why-it-extends-abstractlist-and-key-methods-explained-0898858af45e': 'Understanding Java ArrayList: AbstractList and Core Methods',
    'what-is-bm25-the-ranking-formula-behind-search-engines-c9c79c0a0dbd': 'BM25: How Search Engines Rank Relevant Results',
}


root = ET.parse('/tmp/arshad-medium.xml').getroot()
for item in root.findall('./channel/item'):
    published = datetime.strptime(item.findtext('pubDate'), '%a, %d %b %Y %H:%M:%S %Z')
    title = TITLE_OVERRIDES.get(slug_for(item), html.unescape(item.findtext('title', '').strip()))
    tags = [f"#{category.text.strip().lower().replace(' ', '-')}" for category in item.findall('category')]
    content = item.findtext('{http://purl.org/rss/1.0/modules/content/}encoded', '')
    body = body_to_markdown(content)
    destination = Path('year') / str(published.year) / f'{slug_for(item)}.md'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(f"---\npublished: {published.isoformat()}Z\nsource: medium\nmedium_url: {item.findtext('link').split('?')[0]}\n---\n\n# {title}\n\n{' '.join(tags)}\n\n{body}\n", encoding='utf-8')
    print(destination)