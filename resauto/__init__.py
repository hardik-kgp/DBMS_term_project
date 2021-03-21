from django.db import connection

def setup_database():
    cursor = connection.cursor()
    #create table queries
    orders_query = """CREATE TABLE IF NOT EXISTS orders(
                        order_id INT AUTO_INCREMENT,
                        order_time DATETIME,
                        order_status VARCHAR,
                        order_type VARCHAR,
                        customer_id INT,
                        address_id INT,
                        payment_method VARCHAR,
                        total_bill INT,
                        rating INT,
                        feedback VARCHAR,
                        PRIMARY KEY(order_id),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (address_id) REFERENCES customer_address(address_id)
                    );"""

    #execute all crete queries
    cursor.execute(orders_query)

setup_database()