import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import psycopg2

def scrape():
    blogs=[]
    for page in range(1,18):
        url="https://blog.python.org/blog/" if page == 1 else f"{"https://blog.python.org/blog/"}{page}/"
        response=requests.get("https://blog.python.org/")
        soup=BeautifulSoup(response.text,"html.parser")
        posts=soup.select('a[href^="/20"]')
        for post in posts:
            title=post.get_text(strip=True)
            if not title:
                continue
            blog_url=urljoin("https://blog.python.org/",post.get("href"))

            response=requests.get(blog_url)
            blog_soup=BeautifulSoup(response.text,"html.parser")
            
            main=blog_soup.find("main")

            if main:
                heading=main.find("h1")
                if heading:
                    heading.decompose()
                for element in main.find_all(["header","nav"]):
                    element.decompose()
                info=main.get_text(" ",strip=True)
            
            else:
                info=""

      
            blogs.append({
                "title":title,
                "info":info
            })
    return blogs 
    
def save(blogs):
    conn=psycopg2.connect(
       host="postgres",
       port=5432,
       database="blogs",
       user="postgres",
       password="postgres"
    )
    cursor=conn.cursor()
    for blog in blogs:
        cursor.execute(
            "INSERT INTO blogs (title,info) VALUES (%s,%s)",
            (blog["title"],blog["info"])
        )
    conn.commit()
    cursor.close()
    conn.close()
    print("Blogs saved")


if __name__ == "__main__":
 blogs=scrape()

 print("Total blogs:",len(blogs)) 

 for b in blogs:
    print("Title:",b["title"])
    print("Info:",b["info"])
    print()
 save(blogs)
