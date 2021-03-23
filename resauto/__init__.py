from django.db import connection

def setup_database():
    cursor = connection.cursor()
    #create table queries

    customers = """CREATE TABLE IF NOT EXISTS Customer(
					customer_id INTEGER AUTO_INCREMENT,
                    name VARCHAR(60),
                    email VARCHAR(60),
                    phone char(10),
                    res_coins INTEGER NOT NULL,
                    CHECK (LENGTH(phone) = 10),
                    PRIMARY KEY (customer_id)
				);"""
    
    resources = """CREATE TABLE IF NOT EXISTS Resources(
					resource_id INTEGER AUTO_INCREMENT,
                    name VARCHAR(60),
                    resource_type VARCHAR(60),
                    quantity_present numeric(8,2),
                    unit VARCHAR(20),
                    PRIMARY KEY (resource_id)
				);"""

    employee = """CREATE TABLE IF NOT EXISTS Employee(
					employee_id INTEGER AUTO_INCREMENT,
                    name VARCHAR(60),
                    position VARCHAR(60),
                    salary INTEGER,
                    CHECK (position = "security" or position = "manager" or position = "waiter" or position = "owner" or position = "chef"),
                    PRIMARY KEY (employee_id)
				);"""

    food_item = """CREATE TABLE IF NOT EXISTS food_item(
                    food_id INTEGER AUTO_INCREMENT,
                    name VARCHAR(40),
                    type VARCHAR(40),
                    price INTEGER NOT NULL,
                    is_veg BIT NOT NULL,
                    availability BIT NOT NULL,
                    is_combo BIT NOT NULL,
                    PRIMARY KEY (food_id)
                );"""

    customer_address = """CREATE TABLE IF NOT EXISTS customer_address(
					customer_id INTEGER,
                    address_id INTEGER AUTO_INCREMENT,
                    address VARCHAR(200),
					FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                    PRIMARY KEY (address_id)
				);"""

    orders_query = """CREATE TABLE IF NOT EXISTS orders(
                        order_id INTEGER AUTO_INCREMENT,
                        order_time DATETIME,
                        order_status VARCHAR(40),
                        order_type VARCHAR(40),
                        customer_id INTEGER,
                        address_id INTEGER,
                        payment_method VARCHAR(60),
                        total_bill INTEGER,
                        rating INTEGER,
                        feedback VARCHAR(200),
                        FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                        FOREIGN KEY (address_id) REFERENCES customer_address(address_id),
                        CHECK (order_type in ("DINE-IN","HOME-DELIVERY","PICK-UP")),
                        CHECK (payment_method in ("CASH","CARD","ONLINE")),
                        PRIMARY KEY (order_id)
					);"""

    order_items = """CREATE TABLE IF NOT EXISTS order_items(
					order_id INTEGER,
                    food_id INTEGER,
                    quantity INTEGER,
					FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (food_id) REFERENCES food_item(food_id),
                    PRIMARY KEY (order_id, food_id)
				);"""
    

    order_employee = """CREATE TABLE IF NOT EXISTS order_employee(
					order_id INTEGER,
                    employee_id INTEGER,
					FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
                    PRIMARY KEY (order_id, employee_id)
				);"""

    
    food_combos = """CREATE TABLE IF NOT EXISTS food_combos(
					combo_food_id INTEGER,
                    food_id INTEGER,
                    quantity INTEGER,
					FOREIGN KEY (combo_food_id) REFERENCES food_item(food_id),
                    FOREIGN KEY (food_id) REFERENCES food_item(food_id),
                    PRIMARY KEY (combo_food_id, food_id)
				);"""

    #execute all 9 create queries
    cursor.execute(customers)
    cursor.execute(resources)
    cursor.execute(employee)
    cursor.execute(food_item)
    cursor.execute(customer_address)
    cursor.execute(orders_query)
    cursor.execute(order_items)
    cursor.execute(order_employee)
    cursor.execute(food_combos)


setup_database()