import requests
import psycopg2

name = input("Enter name to search on GitHub: ")

url = "https://api.github.com/search/users"

params = {
    "q": name,
    "per_page": 100
}

headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Mozilla/5.0"
}

try:
    # Search GitHub
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    print("\n========== GITHUB SEARCH RESULT ==========")
    print("Search:", name)
    print("Total results:", data["total_count"])

    # Connect to PostgreSQL
    connection = psycopg2.connect(
        host="psql-db",
        port=5432,
        database="github_data",
        user="postgres",
        password="123456"
    )

    cursor = connection.cursor()

    print("\nUsers found:")

    for i, user in enumerate(data["items"], start=1):

        username = user["login"]
        profile_url = user["html_url"]
        user_type = user["type"]

        print(f"\n{i}. {username}")
        print("   Profile:", profile_url)
        print("   Type:", user_type)

        # Store result in PostgreSQL
        cursor.execute(
            """
            INSERT INTO github_users
            (username, profile_url, user_type)
            VALUES (%s, %s, %s)
            """,
            (username, profile_url, user_type)
        )

    connection.commit()

    print("\n========== DATABASE ==========")
    print("GitHub results stored successfully in PostgreSQL.")

    cursor.close()
    connection.close()

except requests.RequestException as e:
    print("GitHub Error:", e)

except psycopg2.Error as e:
    print("PostgreSQL Error:", e)
