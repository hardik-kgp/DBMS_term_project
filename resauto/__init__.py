from django.db import connection

def setup_database():
    cursor = connection.cursor()
    #create table queries
    orders_query = """CREATE TABLE IF NOT EXISTS orders(
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_time DATETIME,
                        order_status VARCHAR,
                        order_type VARCHAR,
                        customer_id INTEGER,
                        address_id INTEGER,
                        payment_method VARCHAR,
                        total_bill INTEGER,
                        rating INTEGER,
                        feedback VARCHAR,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (address_id) REFERENCES customer_address(address_id)
                    );"""

    #execute all crete queries
    cursor.execute(orders_query)

setup_database()