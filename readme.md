# Log-Analysis

## About
This is the third project for the Udacity Full Stack Nanodegree. In this project, you'll work with data that could have come from a real-world web application, with fields representing information that a web server would record, such as HTTP status codes and URL paths. The web server and the reporting tool both connect to the same database, allowing information to flow from the web server into the report.


----------


## To Run

**Prerequisites:**
-   Python3
-   Vagrant
-   VirtualBox
-
 **Installing**

1.  Install Vagrant And VirtualBox
2.  Clone this repository.
3. Download the data.
4. Unzip the file after downloading. The file inside is newsdata.sql.

**Running the program**

Launch Git shell and redirect to the required directory by running  `vagrant up`, you can then log in with `vagrant ssh`

**Set the Database And Create Views:**

1. To load the data, use the command  `psql -d news -f newsdata.sql`  to connect a database and run the necessary SQL statements.
2. We used a command i.e psql -d news to connect database.
3. Create view using(list of popular articles):
   select articles.title, count(*) as views from articles join log
   on log.path like concat('/article/%',articles.slug)
   group by articles.title order by views desc limit 3;
4. Create view (error) using:
    select ttl.day,((error_3.error_1*100)/ttl.error_2) as prcnt
    from ( select date_trunc('day', time) "day", count(*) as error_1 from
    log where status like '404%' group by day) as error_3
    join( select date_trunc('day',time) "day", count(*) as error_2 from
    log group by day) as ttl on ttl.day =  error_3.day
    where (((error_3.error_1*100)/ttl.error_2)>1)
    order by prcnt desc;


**To execute the program, run `python ./newsdata.py` from the command line.**
