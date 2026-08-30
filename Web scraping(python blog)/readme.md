## Running the Application

1. **Start the Docker Containers**

   First, ensure your Docker containers are up and running:

   ```sh
   docker-compose up
   ```

2. **Access the PostgreSQL Container**

   Open a new terminal and run the following commands:

   ```sh
   docker exec -it scraper_postgres_container sh
   ```

   This command opens an interactive shell inside the PostgreSQL container.

3. **Switch to PostgreSQL User**

   Inside the container, switch to the `postgres` user:

   ```sh
   su - postgres
   ```

4. **Access PostgreSQL CLI**

   Start the PostgreSQL command-line interface:

   ```sh
   psql
   ```

5. **Create the Database**

   Create a new database named `pythondata`:

   ```sh
   create database pythondata;
   ```

6. **Exit the PostgreSQL CLI**

   Exit the PostgreSQL command-line interface:

   ```sh
   exit
   ```

7. **Connect to the Newly Created Database**

   Connect to the `pythondata` database:

   ```sh
   psql -h postgres_service -d pythondata -U postgres
   ```

8. **Enter the Password**

   When prompted, enter the password:

   ```sh
   admin
   ```

9. **Create the Data Table**

   Create a table named `data` to store the scraped blog post details:

   ```sh
   CREATE TABLE data (
       id SERIAL PRIMARY KEY,
       title TEXT,
       date TEXT,
       author TEXT,
       time TEXT,
       file_path TEXT
   );
   ```

10. **Exit the PostgreSQL CLI**

    Exit the PostgreSQL command-line interface:

    ```sh
    exit
    ```

11. **Run the Scraper Script**

    Open another terminal and run the following commands to execute the scraper script inside the Python container:

    ```sh
    sudo docker exec -it scraper_python_container sh
    ```

    This command opens an interactive shell inside the Python container.

12. **Execute the Python Script**

    Run the `main.py` script:

    ```sh
    python main.py
    ```

    The script will start scraping the blog and storing the data in the PostgreSQL database.

13. **Verify the Stored Data**

    You can check the stored data in the PostgreSQL database by running:

    ```sh
    sudo docker exec -it scraper_postgres_container sh
    su - postgres
    psql -h postgres_service -d pythondata -U postgres
    ```

    Enter the password `admin` when prompted. Then, execute the following command to see the data:

    ```sh
    select * from data;
    ```

    This command retrieves all the records stored in the `data` table.

	
