import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import os

conn = psycopg2.connect(
    host="postgres_service",
    database="pythondata",
    user="postgres",
    password="admin")
cursor = conn.cursor()

## Storing the contents in files 
def save_post_to_file(post_content, post_index):
    file_path = f"post_{post_index}.txt"
    with open(file_path, 'w') as file:
        file.write(post_content)
    return file_path

def extract_posts(soup, posts_list, post_index):
    # date
    date_header = soup.find('h2', class_='date-header')
    date = date_header.get_text(strip=True)

    # post-outer div segments each partion
    posts = soup.find_all('div', class_='post-outer')
    for post in posts:
        # Title
        title_tag = post.find('h3', class_='post-title')
        title = title_tag.get_text(strip=True) if title_tag else None
        
        # Author name
        author_tag = post.find('span', class_='post-author')
        author = author_tag.find('span', class_='fn').get_text(strip=True) if author_tag else None
        
        # Time
        time_tag = post.find('span', class_='post-timestamp')
        time = time_tag.find('abbr').get_text(strip=True) if time_tag else None


        post_content = post.get_text(strip=True)
        file_path = save_post_to_file(post_content, post_index)
        
        # storing values in the code
        posts_list.append({
            'Title': title,
            'Date': date,
            'Author': author,
            'Time': time,
            'FilePath': file_path
        })
        
        cursor.execute("""
            INSERT INTO data (title, date, author, time, file_path) 
            VALUES (%s, %s, %s, %s, %s)
        """, (title, date, author, time, file_path))
        conn.commit()

        post_index += 1
        
    return posts_list, post_index

## Function to extract the code of page and call the extract_posts function sending code  of page
def scrape_blog(url, post_index):       
    posts_list = []                                         
    while len(posts_list) < 20:                                                                   
        response = requests.get(url)       
        soup = BeautifulSoup(response.content, 'html.parser')
        posts_list, post_index = extract_posts(soup, posts_list, post_index)
        if len(posts_list) >= 20:          
            break                               
                                                               
        next_button = soup.find('a', class_='blog-pager-older-link')
        if next_button:                                 
            url = next_button['href']                                
        else:               
            break                                           
                                                                                                  
    return posts_list 



### starting call 
posts = scrape_blog('https://blog.python.org/', post_index=1)

## testing part
for post in posts:
    print(f"Title: {post['Title']}")
    print(f"Date: {post['Date']}")
    print(f"Author: {post['Author']}")
    print(f"Time: {post['Time']}")
    print(f"File Path: {post['FilePath']}")
    print('---')