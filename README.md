# DataEngineering-Workshop1
### Workshop 1 Agenda
**Prerequisites**

      Linux Machine
      Docker
      Python 3.10
      PostgreSQL 13
      Beautifulsoup
      urllib2
      requests
      git

1. **Introduction to Docker.**

    - Building the Docker image for Worker using python:3.10.2-alpine3.15
   
    * ***docker***
   
        Docker is a container management service. The keywords of Docker are   develop, ship and run anywhere. The whole idea of Docker is for developers to easily develop applications, ship them into containers which can then be deployed anywhere.
    * ***Images***
   
        Docker images are read-only templates with instructions to create a docker container. Docker image can be pulled from a Docker hub and used as it is, or you can add additional instructions to the base image and create a new and modified docker image. You can create your own docker images also using a dockerfile. Create a dockerfile with all the instructions to create a container and run it; it will create your custom docker image.
    * ***To create docker image for python:3.10.2-alpine3.15***
   
        1)Create a  dockerfile
		
                FROM python:3.10.2-alpine3.15
                # Create directories  
                RUN mkdir -p /root/workspace/src
                # Switch to project directory
                WORKDIR /root/workspace/src

        2)Goto the directory where you created Dockerfile
   
                Docker build -t Simple_python

2. **Introduction to Webscrapping.**
    - **Beautifulsoup**
      - *Introduction*       
          Beautiful Soup is a python package which allows us to pull  data out of HTML and XML documents.
      - *Beautiful Soup - Installation*
      
          pip install beautifulsoup4
      - *Import beautifulsoup*
      
          from bs4 import BeautifulSoup
      - *Important Methods*
                        
        1) **find**(name, attrs, recursive, string, **kwargs)
      
           scan the entire document to find only one result.

        2) **find_all**(name, attrs, recursive, string, limit, **kwargs)
     
           You can use find_all to extract all the occurrences of a particular tag from the page response as

    - **Regex**
   
        ***Introduction***
   
        The Python module re provides full support for Perl-like regular expressions in Python
   
        ***Important methods***
   
        * **re.match**(pattern, string, flags=0)
   
          The re.match function returns a match object on success, None on failure. We usegroup(num) or groups() function of the match object to get a matched expression
   
        * **re.search**(pattern, string, flags=0)
   
          The search() function searches the string for a match, and returns a Match object if there is a match.
   
        * **re.findall**(pattern, string, flags=0))
   
          function returns a list containing all matches.
   
        * **re.sub**(pattern,replace_string,string)
   
          The sub() function replaces the matches with the text of your choice:
   
       ***Metacharacters***
   
                        []	a set of a character
                        .	 any character
                        ^	start with
                        $ 	end with
                        * 	zero or more occurrences
                        +	one or more occurrences
                        ?	zero or one occurrences
                        {}	exactly specified number of occurrence
                        () 	capture a group
                *Important Special Sequences*
                        \w		Matches word characters.
                        \W		Matches nonword characters.
                        \s		Matches whitespace. Equivalent to [\t\n\r\f].
                        \S	           Matches nonwhitespace	
                        \d		Matches digits. Equivalent to [0-9].
                        \D		Matches Nondigits
    - urllib2/requests 
   
        ***Request***
   
            Introduction
   
                The requests module allows you to send HTTP requests using Python.
   
            Importent Methods
   
                1)get(url,params,args)
                        Sends a GET request to the specified url
                2)Post(url,data,json,args)
                        Sends a POST request to the specified url
                3)delete(url,args)
                        Sends a DELETE request to the specified url
        ***Urllib***
   
            Introduction
            It is a Python 3 package that allows you to access, and interact with, websites using their URL’s (Uniform Resource Locator). It has several modules for working with URL’s, these are shown in the illustration below:	
			
            Urllib.request
                Using urllib.request, with urlopen, allows you to open the specified URL.
            Urllib.error
                This module is used to catch exceptions encountered from url.request

    - **Writing a script using the above packages and run it in Docker**.
   
           *web_scraping_sample.py*
            import requests
            from bs4 import BeautifulSoup
            import re
            res = requests.get('https://www.lipsum.com/')
            soup = BeautifulSoup(res.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
            data=soup.find(re.compile(r'div'),attrs={'id':"Panes"})
            print(data.find("lorem"))
            qes_list=[]
            ans_list=[]
            for row in data.findAll("div"):
                qes_list.append(row.h2.text)
                tempstring=""
                counter=0
                for i in row.findAll("p"):
                    tempstring=tempstring+"\n"+i.text
                ans_list.append(tempstring)
            tempstring=""
            for i in range(len(qes_list)):
                tempstring=tempstring+"\n"+qes_list[i]+"\n"+ans_list[i]+"\n--------------------------------------------------------------------------------------------------\n\n"
                print(tempstring)
		
        ***Creating a dockerfile in same directory***
		
            FROM python:3.10.2-alpine3.15
            # Create directories  
            RUN mkdir -p /root/workspace/src
            COPY ./web_scraping_sample.py  /root/workspace/src
            # Switch to project directory
            WORKDIR /root/workspace/src
            RUN python web_scraping_sample.py
    - ***Build dokcer image***
   
         docker build -t simple_python
    - ***Run image as a docker container***
   
         docker run -d  --name container1 simple_python



 3. **Introduction to PostgreSQL.**
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
             COPY ./one.py  /root/workspace/src
             # Switch to project directory
             WORKDIR /root/workspace/src
             RUN python web_scraping_sample.py

            Goto the directory where you created Dockerfile
                Docker build -t simple_python

 4. **Introduction to Github.**
     - **Setting up github**.
   
         Make a repository in GitHub
   
             Go to GitHub.com and login.
             Click the green “New Repository” button
                     Repository name: myrepo
                     Public
                     Check Initialize this repository with a README
                     Click the green “Create repository” button
             Copy the HTTPS clone URL to your clipboard via the green “Clone or Download” button.
         Clone the repository to your computer
   
             git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
			
         Make a local change, commit, and push
   
             git add <file path>	//here the file path is which file you modified ready the file for commit
             git commit -m "A commit from my local computer"	      //here you commit the changes
             git push origin <brachname> 	//here you push the changes to your remote repository and brach name is in which brach you pushing this
     - **Basic commands of git**
   
         * **git init**
      
            he command git init is used to create an empty Git repository.
   
         * **git add**
      
             Add command is used after checking the status of the files, to add t	hose files to the staging area.
             Before running the commit command, "git add" is used to add any new or modified files.
   
         * **git commit**
      
             The commit command makes sure that the changes are saved to the local repository.
             The command "git commit –m <message>" allows you to describe everyone and help them understand what has happened.
         * **git status**
      
             The git status command tells the current state of the repository.
      
             The command provides the current working branch. If the files are in the staging area, but not committed, it will be shown by the git status. Also, if there are no changes, it will show the message no changes to commit, working directory clean.
         * **git config**
      
           The git config command is used initially to configure the user.name and user.email. This specifies what email id and username will be used from a local repository.

 5. **Workshop 1 Home Work.**

         A PR should be given where the data is scrapped from Lorem Ipsum - All the facts - Lipsum generator[ Lorem Ipsum - All the facts - Lipsum generator](https://www.lipsum.com/)   website and save each section from that page in the database.
