#!/usr/bin/env python3
"""Embed problem Markdown from a local MAIS checkout; never fetch at page load."""
import argparse
import html
import re
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlsplit, quote
import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Math-for-AI-Safety/MAIS'
MATH = re.compile(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?:\\.|[^$])+?(?<!\\)\$')

def render(source, filename, revision):
    expressions = []
    def protect(match):
        expressions.append(match.group())
        return f'MAISMATHTOKEN{len(expressions)-1}END'
    source = re.sub(r'^# [^\n]+\n', '', source, count=1)
    body = markdown.markdown(MATH.sub(protect, source), extensions=['tables', 'fenced_code', 'toc', 'sane_lists'])
    for i, expression in enumerate(expressions):
        body = body.replace(f'MAISMATHTOKEN{i}END', html.escape(expression))
    fragment = BeautifulSoup(body, 'html.parser')
    for tag in fragment.find_all(['a', 'img']):
        attr = 'href' if tag.name == 'a' else 'src'
        target = tag.get(attr, '')
        parts = urlsplit(target)
        if parts.scheme or target.startswith(('#', '//')):
            continue
        problem = re.fullmatch(r'(?:\./|../open-problems/)?(MAIS-O\d+)\.md', parts.path)
        if problem and (ROOT / 'wiki/p' / (problem[1] + '.html')).exists():
            tag[attr] = problem[1] + '.html' + ('#' + parts.fragment if parts.fragment else '')
        else:
            tag[attr] = urljoin(f'{REPO}/blob/{revision}/open-problems/{filename}', target)
    return str(fragment)

def sync(checkout):
    revision = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
    pages = sorted((ROOT / 'wiki/p').glob('MAIS-O*.html'))
    for page in pages:
        source = checkout / 'open-problems' / (page.stem + '.md')
        if not source.exists():
            raise FileNotFoundError(source)
        soup = BeautifulSoup(page.read_text(), 'html.parser')
        main = soup.find('main')
        crumbs = main.find(class_='crumbs').extract()
        title = main.find('h1').extract()
        metadata = main.find(class_='meta').extract()
        info = main.find(class_='infobox').extract()
        related = main.find(id='related')
        related_nodes = []
        if related:
            related_nodes = [related, *list(related.next_siblings)]
            for node in related_nodes:
                node.extract()
        main.clear()
        main['class'] = ['problem-page']
        for node in [crumbs, title, metadata]:
            main.append(node)
        actions = soup.new_tag('nav', attrs={'class':'page-actions', 'aria-label':'Problem actions'})
        for label, url in [('View source', f'{REPO}/blob/main/open-problems/{source.name}'), ('Discuss', f'{REPO}/issues?q=' + quote('is:issue ' + page.stem)), ('Suggest an edit', f'{REPO}/edit/main/open-problems/{source.name}')]:
            a = soup.new_tag('a', href=url)
            a.string = label
            actions.append(a)
        main.append(actions)
        # The title spans the page; metadata no longer competes with it.
        info['class'] = ['infobox', 'problem-metadata']
        info['aria-label'] = 'Problem metadata'
        main.append(info)
        article = soup.new_tag('article', attrs={'class':'problem-statement', 'aria-label':'Full problem statement'})
        article.append(BeautifulSoup(render(source.read_text(), source.name, revision), 'html.parser'))
        main.append(article)
        credit = soup.new_tag('p', attrs={'class':'source-credit'})
        credit.append('Adapted to HTML from ')
        a = soup.new_tag('a', href=f'{REPO}/blob/{revision}/open-problems/{source.name}')
        a.string = 'MAIS source · ' + revision[:7]
        credit.append(a)
        credit.append('. Original authorship is credited above. Licensed under ')
        a = soup.new_tag('a', href=f'{REPO}/blob/{revision}/LICENSE')
        a.string = 'CC BY 4.0'
        credit.append(a)
        credit.append('.')
        main.append(credit)
        for node in related_nodes:
            main.append(node)
        page.write_text(str(soup))
    print(f'Embedded {len(pages)} statements from MAIS {revision[:7]}.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, help='Local checkout of Math-for-AI-Safety/MAIS')
    sync(parser.parse_args().checkout.resolve())
