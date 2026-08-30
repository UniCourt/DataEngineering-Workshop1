import requests
from bs4 import BeautifulSoup
import re
import psycopg2
from psycopg2 import Error

url = 'https://blog.python.org/'

def create_connection(db_name, db_user, db_password, db_host, db_port):
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def execute_query(connection, data):
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO python_blog_articles (date, title, body, author)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_table(connection):
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS python_blog_articles (
            id SERIAL PRIMARY KEY,
            date VARCHAR(100),
            title TEXT,
            body TEXT,
            author VARCHAR(100)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully or already exists")
    except Error as e:
        print(f"The error '{e}' occurred")

def process_page(soup, date, titletext, bodytext, author):
    for div in soup.find_all('div', class_='date-outer'):
        date_header = div.find('h2', class_='date-header')
        if date_header:
            date_text = date_header.find('span').get_text(strip=True)
            date.append(date_text)
        
        for post in div.find_all('div', class_='post-outer'):
            title_head = post.find('h3', class_='post-title entry-title')
            if title_head:
                titletext.append(title_head.text.strip())
            
            content_div = post.find('div', class_='post-body entry-content')
            if content_div:
                paragraph_text = ' '.join([p.text.strip() for p in content_div.find_all('p')])
                bodytext.append(paragraph_text)

            footer_head = post.find('div', class_='post-footer')
            if footer_head:
                footer_text = footer_head.find('span', class_='post-author vcard').text.strip()
                author.append(footer_text)

def main():
    db_name = 'webdemo'
    db_user = 'postgres'
    db_password = '123456'
    db_host = 'localhost'
    db_port = '5434'

    connection = create_connection(db_name, db_user, db_password, db_host, db_port)

    if connection:
        try:
            date = []
            titletext = []
            bodytext = []
            author = []

            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html5lib')
            process_page(soup, date, titletext, bodytext, author)

            while len(titletext) < 50:
                older_posts_link = soup.find('a', string=re.compile(r'Older Posts', re.IGNORECASE))
                if older_posts_link:
                    next_page_url = older_posts_link['href']
                    res = requests.get(next_page_url)
                    soup = BeautifulSoup(res.content, 'html5lib')
                    process_page(soup, date, titletext, bodytext, author)
                else:
                    break
            
            create_table(connection)
            for i in range(len(titletext)):
                data = (date[i], titletext[i], bodytext[i], author[i])
                execute_query(connection, data)

        except Error as e:
            print(f"Error: {e}")

        finally:
            if connection:
                connection.close()
                print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()
