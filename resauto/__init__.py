from django.db import connection

def setup_database():
    cursor = connection.cursor()
    #create table queries
    orders_query = """CREATE TABLE IF NOT EXISTS orders_test(
                        order_id INT(10)
                    )"""

    #execute all crete queries
    cursor.execute(orders_query)

setup_database()