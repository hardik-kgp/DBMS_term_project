from django.db import connection
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
	def __init__(self, name, position, salary):
		self.employee_id = -1
		self.name = name
		self.position = position
		self.salary = salary
		self.user = models.OneToOneField(User, on_delete=models.CASCADE)

	def insert(self):
		cursor = connection.cursor()
		query = """INSERT INTO Employee
					(name, position, salary)
					VALUES ('{0}','{1}','{2}')""".format(
				self.name,
				self.position,
				self.salary,
		)
		cursor.execute(query)

		query = """SELECT LAST_INSERT_ID();"""
		cursor.execute(query)
		rows = cursor.fetchall()
		for row in rows:
			self.employee_id = row[0]

		print("My employee is entered into the table and is ready to rock!")

	def update(self):
		cursor = connection.cursor()
		query = """UPDATE TABLE Employee SET
					name='{0}',
					position='{1}',
					salary='{2}',
					WHERE employee_id={3};
				""".format(
				self.name,
				self.position,
				self.salary,
				self.employee_id
		)
		cursor.execute(query)

	@staticmethod
	def find(eid):
		cursor = connection.cursor()
		query = """SELECT employee_id, name, position, salary
					FROM Employee WHERE employee_id='{0}'
				""".format(
				eid
		)
		cursor.execute(query)
		rows = cursor.fetchall()
		employee = []
		for row in rows:
			# print("len of row is: ", len(row))
			o = Employee(row[1], row[2], row[3])
			o.employee_id = row[0]
			employee.append(o)
		return employee[0]

	@staticmethod
	def find_all():
		cursor = connection.cursor()
		query = """SELECT employee_id, name, position, salary
					FROM Employee
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		employee = []
		for row in rows:
			# print("len of row is: ", len(row))
			o = Employee(row[1], row[2], row[3])
			o.employee_id = row[0]
			employee.append(o)
		return employee

	@staticmethod
	def delete(eid):
		cursor = connection.cursor()
		query = """DELETE FROM Employee WHERE employee_id='{0}'""".format(
			eid
		)
		cursor.execute(query)

	@staticmethod
	def get_average_rating(eid):
		cursor = connection.cursor()
		query = """
				select avg(rating)
				from orders
				where orders.order_id in (select order_id 
										from order_employee 
										where order_employee.employee_id = '{0}') """.format(eid)
		cursor.execute(query)
		rows = cursor.fetchall()
		return rows[0][0]

	# @staticmethod
	# def get_all_feedbacks(eid):

	# 	cursor = connection.cursor()
	# 	query = """
	# 			select feedback
	# 			from orders
	# 			where orders.order_id in (select order_id
	# 									from order_employee
	# 									where order_employee.employee_id = '{0}') """.format(eid)
	# 	cursor.execute(query)
	# 	rows = cursor.fetchall()
	# 	rows = [row[0] for row in rows]
	# 	return rows

	@staticmethod
	def get_best_employee():

		cursor = connection.cursor()
		query = """
				Select *
				from (
						select temp.employee_id, temp.name, avg(temp.rating) as emp_rating
						from (select Employee.employee_id, Employee.name, orders.rating
						from Employee, order_employee, orders
						where Employee.employee_id = order_employee.employee_id and order_employee.order_id = orders.order_id) as temp
						
						group by temp.employee_id, temp.name ) as T
				order by T.emp_rating DESC
				LIMIT 1;					
				"""

		cursor.execute(query)
		rows = cursor.fetchall()

		if(len(rows) == 0):
			return ("null", 0)
		else:
			return (rows[0][1], rows[0][2])

	@staticmethod
	def insert_random_employees(oid):
		cursor = connection.cursor()

		query = """SELECT * FROM Employee order by rand() limit 2"""

		cursor.execute(query)

		rows = cursor.fetchall()

		id1, id2 = rows[0][0], rows[1][0]

		query = """ insert into order_employee values ('{0}','{1}')""".format(
			oid, id1)
		cursor.execute(query)

		query = """ insert into order_employee values ('{0}','{1}')""".format(
			oid, id2)
		cursor.execute(query)


class Customer(models.Model):
	def __init__(self, name, email, phone, res_coins, balance):
		self.customer_id = -1
		self.name = name
		self.email = email
		self.phone = phone
		self.res_coins = res_coins
		self.balance = balance
		self.user = models.OneToOneField(User, on_delete=models.CASCADE)

	def insert(self):
		cursor = connection.cursor()
		query = """INSERT INTO Customer
					(name, email, phone, res_coins, balance)
					VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(
				self.name,
				self.email,
				self.phone,
				self.res_coins,
				self.balance
		)
		cursor.execute(query)
		query = """SELECT LAST_INSERT_ID();"""
		cursor.execute(query)
		rows = cursor.fetchall()
		for row in rows:
			self.customer_id = row[0]

	def update(self):
		cursor = connection.cursor()
		query = """UPDATE Customer SET
					name='{0}',
					email='{1}',
					phone='{2}',
					res_coins='{3}',
					balance = '{5}'
					WHERE customer_id={4};
				""".format(
				self.name,
				self.email,
				self.phone,
				self.res_coins,
				self.customer_id,
				self.balance
		)
		cursor.execute(query)

	@staticmethod
	def find(cid):
		cursor = connection.cursor()
		query = """SELECT customer_id, name, email, phone, res_coins, balance
					FROM Customer WHERE customer_id='{0}'
				""".format(
				cid
		)
		cursor.execute(query)
		rows = cursor.fetchall()
		customer = []
		for row in rows:
			o = Customer(row[1], row[2], row[3], row[4], row[5])
			o.customer_id = row[0]
			customer.append(o)
		return customer[0]

	@staticmethod
	def find_all():
		cursor = connection.cursor()
		query = """SELECT customer_id, name, email, phone, res_coins, balance
				   FROM Customer
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		customer = []
		for row in rows:
			o = Customer(row[1], row[2], row[3], row[4])
			o.customer_id = row[0]
			customer.append(o)
		return customer

	@staticmethod
	def delete(cid):
		cursor = connection.cursor()
		query = """DELETE FROM Customer WHERE customer_id='{0}'""".format(
			cid
		)
		cursor.execute(query)


class Address():
	def __init__(self, customer_id, address):
		self.address_id = -1
		self.customer_id = customer_id
		self.address = address

	@staticmethod
	def add_address(cid, address):
		cursor = connection.cursor()
		query = """INSERT INTO customer_address (customer_id, address) VALUES ('{0}','{1}');""".format(
			cid, address)
		cursor.execute(query)

	@staticmethod
	def get_addresses(cid):
		cursor = connection.cursor()
		query = """ SELECT * FROM customer_address WHERE customer_id='{0}'""".format(
			cid)
		cursor.execute(query)
		rows = cursor.fetchall()

		addresses = []
		for row in rows:
			add = Address(row[0], row[2])
			add.address_id = row[1]
			addresses.append(add)

		return addresses

	@staticmethod
	def get_address_from_id(aid):
		cursor = connection.cursor()
		query = """ SELECT address FROM customer_address WHERE address_id='{0}'""".format(
			aid)
		cursor.execute(query)
		rows = cursor.fetchall()

		return rows[0][0]


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	customer_id = models.IntegerField()
	type = models.CharField(max_length = 50)
	
	def __str__(self):
		return self.user.username



	def __str__(self):
		return self.user.username
