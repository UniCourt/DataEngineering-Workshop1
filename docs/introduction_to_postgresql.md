### Introduction to PostgreSQL.
     - **Key Features of PostgreSQL**.
        - Free to download
        - Compatible with Data Integrity
        - Compatible with multiple data types
        - Highly extensible
        - Secure
        -  Highly Reliable:
 	
     - **JOINS**.
        - The CROSS JOIN
        - The INNER JOIN
        - The LEFT OUTER JOIN
        - The RIGHT OUTER JOIN
        - The FULL OUTER JOIN
        ![Pictorial Representation of JOINS](https://i.stack.imgur.com/4zjxm.png)
        
       **The CROSS JOIN**
    
           A CROSS JOIN matches every row of the first table with every row of the second table
           SELECT ... FROM table1 CROSS JOIN table2 …
           SELECT EMP_ID, NAME, DEPT FROM COMPANY CROSS JOIN DEPARTMENT;
			
       **The INNER JOIN**
    
           A INNER JOIN creates a new result table by combining column values of two tables (table1 and table2) based upon the join-predicate. The query compares each row of table1 with each row of table2 to find all pairs of rows, which satisfy the join-predicate. When the join-predicate is satisfied, column values for each matched pair of rows of table1 and table2 are combined into a result row.
           SELECT table1.column1, table2.column2...
           FROM table1
           INNER JOIN table2
           ON table1.common_filed = table2.common_field;
			
           SELECT EMP_ID, NAME, DEPT FROM COMPANY INNER JOIN DEPARTMENT ON COMPANY.ID = DEPARTMENT.EMP_ID;
			
       **The LEFT OUTER JOIN**
    
           The OUTER JOIN is an extension of the INNER JOIN. SQL standard defines three types of OUTER JOINs: LEFT, RIGHT, and FULL and PostgreSQL supports all of these.
           In case of LEFT OUTER JOIN, an inner join is performed first. Then, for each row in table T1 that does not satisfy the join condition with any row in table T2, a joined row is added with null values in columns of T2. Thus, the joined table always has at least one row for each row in T1.
			
           SELECT ... FROM table1 LEFT OUTER JOIN table2 ON conditional_expression ...
			
           SELECT EMP_ID, NAME, DEPT FROM COMPANY LEFT OUTER JOIN DEPARTMENT
           ON COMPANY.ID = DEPARTMENT.EMP_ID;
			
       **The RIGHT OUTER JOIN**
    
           First, an inner join is performed. Then, for each row in table T2 that does not satisfy the join condition with any row in table T1, a joined row is added with null values in columns of T1. This is the converse of a left join; the result table will always have a row for each row in T2.
           SELECT ... FROM table1 RIGHT OUTER JOIN table2 ON conditional_expression ...
			
           SELECT EMP_ID, NAME, DEPT FROM COMPANY RIGHT OUTER JOIN DEPARTMENT  ON COMPANY.ID = DEPARTMENT.EMP_ID;
		
       **The FULL OUTER JOIN**
    
           First, an inner join is performed. Then, for each row in table T1 that does not satisfy the join condition with any row in table T2, a joined row is added with null values in columns of T2. In addition, for each row of T2 that does not satisfy the join condition with any row in T1, a joined row with null values in the columns of T1 is added.
           The following is the syntax of FULL OUTER JOIN −
               SELECT ... FROM table1 FULL OUTER JOIN table2 ON conditional_expression ...
           Based on the above tables, we can write an inner join as follows −
               SELECT EMP_ID, NAME, DEPT FROM COMPANY FULL OUTER JOIN DEPARTMENT   ON COMPANY.ID = DEPARTMENT.EMP_ID;
     - **Things to Note**
    
         - You can do select with limit 
         - You are able to do group by, order by ,having clauses, etc.
         - Your not able to limit delete and update directly. You need to use inner query
             > delete from  student where sid in (select id from table limit 10)
           
             > update from  student set city=”mangalore”where sid in (select id from table limit 10)

     - **Update the existing docker image to support PostgreSQL**
     
             FROM python:3.10.2-alpine3.15
             RUN apk update
             RUN apk add postgresql
             RUN chown postgres:postgres /run/postgresql/
             # Create directories  
             RUN mkdir -p /root/workspace/src
             COPY ./web_scraping_sample.py  /root/workspace/src
             # Switch to project directory
             WORKDIR /root/workspace/src

            Goto the directory where you created Dockerfile
                Docker build -t simple_python
