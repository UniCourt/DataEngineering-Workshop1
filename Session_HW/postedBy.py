# postedBy.py
import requests
from bs4 import BeautifulSoup

def get_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_posted_by(soup):
    posted_by = []
    post_footer_divs = soup.find_all('div', class_='post-footer-line post-footer-line-1')
    for post_footer_div in post_footer_divs:
        span_tag = post_footer_div.find('span', class_='fn')
        if span_tag:
            posted_by_name = span_tag.text.strip()
            posted_by.append(posted_by_name)
    return posted_by

def extract_authors_from_content(content):
    extracted_phrases = []
    found_release_team = False

    release_team_positions = [pos for pos in range(len(content)) if content.lower().find('release team,', pos) == pos]
    
    if release_team_positions:
        pos = release_team_positions[-1] + len('release team,')
        after_release_team = content[pos:].strip()
        if after_release_team:
            lines = after_release_team.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    extracted_phrases.append(line)

    if extracted_phrases:
        return ', '.join(extracted_phrases)
    return None

def extract_authors(soup):
    authors_list = []
    post_body_divs = soup.find_all('div', class_='post-body entry-content')
    for post_body_div in post_body_divs:
        content = post_body_div.get_text(separator='\n', strip=True)
        authors = extract_authors_from_content(content)
        if authors:
            authors_list.append(authors)
    return authors_list

def get_older_posts_url(soup):
    older_posts_link = soup.find('a', class_='blog-pager-older-link')
    return older_posts_link['href'] if older_posts_link else None

def your_function_that_returns_data():
    base_url = 'https://blog.python.org/'

    posted_by_list = []
    author_list = []
    date_list = []
    pythonVersionsBlogs = []
    pythonVersionsBlogLinks = []
    version_href_list = []

    current_url = base_url

    blogs_processed = 0
    max_blogs = 50

    while blogs_processed < max_blogs:
        soup = get_content(current_url)
        
        posted_by = extract_posted_by(soup)
        posted_by_list.extend(posted_by)
        
        authors = extract_authors(soup)
        author_list.extend(authors)
        
        data = soup.find_all('div', attrs={'class': 'date-outer'})
        for section in data:
            date_header = section.find('h2', class_='date-header')
            if date_header:
                date = date_header.text.strip()
            else:
                date = "No date"
            
            posts = section.find_all('div', class_='post hentry')
            for post in posts:
                date_list.append(date)
                pythonVersionsBlog = post.find('h3', class_='post-title entry-title').text.strip()
                pythonVersionsBlogs.append(pythonVersionsBlog)
                pythonVersionsBlogLinkTag = post.find('h3', class_='post-title entry-title').find('a', href=True)
                pythonVersionsBlogLink = pythonVersionsBlogLinkTag['href']
                pythonVersionsBlogLinks.append(pythonVersionsBlogLink)
        
        elements = soup.find_all(class_='post-body entry-content')
        for element in elements:
            links = element.find_all('a', href=True)
            filtered_links = []
            for link in links:
                href = link['href']
                if href.startswith('https://www.python.org/downloads/release/python'):
                    filtered_links.append(href)
            if filtered_links:
                version_href_list.append(','.join(filtered_links))
            else:
                version_href_list.append("No links found")
        
        blogs_processed += min(len(posted_by), len(authors), len(date_list), len(pythonVersionsBlogs), len(pythonVersionsBlogLinks), len(version_href_list))
        
        if blogs_processed >= max_blogs:
            break
        
        current_url = get_older_posts_url(soup)
        if not current_url:
            break

    posted_by_list = posted_by_list[:max_blogs]
    author_list = author_list[:max_blogs]
    date_list = date_list[:max_blogs]
    pythonVersionsBlogs = pythonVersionsBlogs[:max_blogs]
    pythonVersionsBlogLinks = pythonVersionsBlogLinks[:max_blogs]
    version_href_list = version_href_list[:max_blogs]

    return date_list, pythonVersionsBlogs, pythonVersionsBlogLinks, version_href_list, author_list, posted_by_list
