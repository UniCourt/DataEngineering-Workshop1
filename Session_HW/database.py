import psycopg2
from postedBy import your_function_that_returns_data 

def insert_data_into_postgres(date_list, pythonVersionsBlogs, pythonVersionsBlogLinks, version_href_list, author_list, posted_by_list):
    conn_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': '123456',
        'host': 'psql-db',
        'port': '5432'
    }

    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS blog_data (
            id SERIAL PRIMARY KEY,
            date TEXT,
            blog_title TEXT,
            blog_link TEXT,
            version_links TEXT,
            authors TEXT,
            posted_by TEXT
        );
        """
        cur.execute(create_table_query)

        # Insert data
        for i in range(len(date_list)):
            insert_query = """
            INSERT INTO blog_data (date, blog_title, blog_link, version_links, authors, posted_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(insert_query, (
                date_list[i],
                pythonVersionsBlogs[i],
                pythonVersionsBlogLinks[i],
                version_href_list[i],
                author_list[i],
                posted_by_list[i]
            ))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Extract data
    date_list, pythonVersionsBlogs, pythonVersionsBlogLinks, version_href_list, author_list, posted_by_list = your_function_that_returns_data()

    insert_data_into_postgres(date_list, pythonVersionsBlogs, pythonVersionsBlogLinks, version_href_list, author_list, posted_by_list)

if __name__ == "__main__":
    main()
