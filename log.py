# !/usr/bin/emv python3
import psycopg2

# 1.The list of popular articles:
query_1 = """select articles.title, count(*) as views from articles join log
        on log.path like concat('/article/%',articles.slug)
        group by articles.title order by views desc limit 3;"""

# 2.The list of popular authors:
query_2 = """select authors.name, count(*) as views from authors join articles
        on authors.id = articles.author join log
        on log.path like concat('/article/%',articles.slug)
        group by authors.name order by views desc limit 4; """

# 3.On which days did more than 1% of requests lead to errors?
query_3 = """select ttl.day,((error_3.error_1*100)/ttl.error_2) as prcnt
          from ( select date_trunc('day', time) "day", count(*) as error_1 from
          log where status like '404%' group by day) as error_3
          join( select date_trunc('day',time) "day", count(*) as error_2 from
          log group by day) as ttl on ttl.day =  error_3.day
          where (((error_3.error_1*100)/ttl.error_2)>1)
          order by prcnt desc;"""

# Storing Results
q1_result = dict()
q1_result_title = "\n1.What are the most popular three articles of all time?"
q2_result = dict()
q2_result_title = "\n2.Who are the most popular article authors of all time?"
q3_result = dict()
q3_result_title = "\n3.On which days did more than 1% request lead to errors?"

DATABASE = "news"


# Query Result
def query_result(query):
    db = psycopg2.connect(database=DATABASE)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_results(query_result, title):
    print (title)
    for result in query_result['results']:
        print('\t' + str(result[0]) + ' ---> ' + str(result[1]) + ' views')


def print_error_results(query_result, title):
    print (title)
    for result in query_result['results']:
        string = str(result[0])
        out = string[: 10]
        print('\t' + out + ' ---> ' + str(result[1]) + ' % ')

# storing Query Result
q1_result['results'] = query_result(query_1)
q2_result['results'] = query_result(query_2)
q3_result['results'] = query_result(query_3)

# print Output
print_results(q1_result, q1_result_title)
print_results(q2_result, q2_result_title)
print_error_results(q3_result, q3_result_title)
