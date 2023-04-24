import psycopg2
import csv
conn = psycopg2.connect(
    host="172.17.0.2",
    port="5432",
    dbname="demodb",
    user="postgres",
    password="123456"
)

cur = conn.cursor()

with open('output.csv','r') as f:
 csv_reader = csv.reader(f)
 next(csv_reader)
 for row in csv_reader:
     if row[1] =="":
       row[1] = "N/A"
   
     cur.execute("INSERT INTO demotable (column1, column2, column3) VALUES (%s, %s, %s)",(row[0], row[1],row[2]))

conn.commit()

cur.close()
conn.close()
