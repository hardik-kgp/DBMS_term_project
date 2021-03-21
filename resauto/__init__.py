from django.db import connection

def setup_database():
    cursor = connection.cursor()
    #create table queries
    orders_query = """CREATE TABLE IF NOT EXISTS orders(
                        order_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        order_time DATETIME,
                        order_status VARCHAR(40),
                        order_type VARCHAR(40),
                        customer_id INTEGER,
                        address_id INTEGER,
                        payment_method VARCHAR(60),
                        total_bill INTEGER,
                        rating INTEGER,
                        feedback VARCHAR(200),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (address_id) REFERENCES customer_address(address_id)
                    );"""

    food_item = """CREATE TABLE IF NOT EXISTS food_item(
                    food_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(40),
                    type VARCHAR(40),
                    price INTEGER NOT NULL,
                    is_veg BIT NOT NULL,
                    availability INTEGER NOT NULL,
                    is_combo BIT NOT NULL
                );"""

    #execute all crete queries
    # cursor.execute(orders_query)


setup_database()