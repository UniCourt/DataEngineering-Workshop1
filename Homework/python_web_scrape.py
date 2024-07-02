import requests
from bs4 import BeautifulSoup
import re
import psycopg2
from psycopg2 import Error

url = 'https://blog.python.org/'

# If this line causes an error, run 'pip install html5lib' or install html5lib

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Function to execute insert queries
def execute_query(connection,data):
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
    try:
        cursor = connection.cursor()
        # SQL statement to create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS python_blog_articles (
            id SERIAL PRIMARY KEY,
            date VARCHAR(100),
            title TEXT,
            body TEXT,
            author VARCHAR(100)
        );
        """
        # Execute the SQL query
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully or already exists")
    except Error as e:
        print(f"The error '{e}' occurred")

date=[]
titletext=[]
bodytext=[]
author=[]

# Find all <div> elements with class="date-outer"
def process_page(soup):
    for div in soup.find_all('div', class_='date-outer'):
        hd = div.find_all('div', 'post-outer')
        for i in hd:
            date_header = div.find('h2', class_='date-header')
            if date_header:
                date_text = date_header.find('span')
                dt = date_text.get_text(strip=True)
                date.append(dt)
        tdiv = div.find('div', class_='date-posts')
        for div1 in tdiv.find_all('div', class_='post-outer'):
            title_head = div1.find('h3', class_='post-title entry-title')
            if title_head:
                title_text = title_head.text.strip()
                titletext.append(title_text)
            content_div = div1.find('div', class_='post-body entry-content')
            if content_div:
                for p_tag in content_div.find_all('p'):
                    paragraph_text = content_div.text.strip()
                    cleaned_content = re.sub(r'\n+', ' ', paragraph_text)
                bodytext.append(cleaned_content)
        foot = div.find_all('div', class_='post-outer')
        for i in foot:
            footer_head = div.find('div', class_='post-footer')
            footer_text = footer_head.find('span', class_='post-author vcard').text.strip()
            cleanedf_content = re.sub(r'\n+', ' ', footer_text)
            author.append(cleanedf_content)




def main():
    # PostgreSQL database connection settings
    db_name = 'webdemo'
    db_user = 'postgres'
    db_password = '123456'
    db_host = 'localhost'  # or your host
    db_port = '5434'  # or your port

    # Establish connection to PostgreSQL
    connection = create_connection(db_name, db_user, db_password, db_host, db_port)

    if connection:
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html5lib')
            process_page(soup
            )
            
            # Scraping subsequent pages until we have 50 articles
            while len(titletext) < 50:
                older_posts_link = soup.find('a', string=re.compile(r'Older Posts', re.IGNORECASE))
                if older_posts_link:
                    next_page_url = older_posts_link['href']
                    res = requests.get(next_page_url)
                    soup = BeautifulSoup(res.content, 'html5lib')
                    process_page(soup)
                else:
                    break
            
            create_table(connection)
            for i in range(len(titletext)):
                data = (date[i], titletext[i], bodytext[i], author[i])
                execute_query(connection,data)


        except Error as e:
            print(f"Error: {e}")

        finally:
            if connection:
                connection.close()
                print("PostgreSQL connection is closed")

if __name__ == "__main__":
    main()