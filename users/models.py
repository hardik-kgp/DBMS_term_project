from django.db import connection

# Create your models here.
class Employee():
	def __init__(self, name, position, salary):
		self.employee_id=-1
		self.name=name
		self.position=position
		self.salary=salary

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
		# self.employee_id =  #GET ORDER ID HERE FROM QUERY SOMEHOW

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
		Employee = []
		for row in rows:
			o = Employee(row[1],row[2],row[3])
			o.employee_id = row[0]
			Employee.append(o)
		return Employee[0]

	@staticmethod
	def find_all():
		cursor = connection.cursor()
		query = """SELECT employee_id, name, position, salary
					FROM Employee
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		Employee = []
		for row in rows:
			o = Employee(row[1],row[2],row[3])
			o.employee_id = row[0]
			Employee.append(o)
		return Employee

	@staticmethod
	def delete(eid):
		cursor = connection.cursor()
		query = """DELETE FROM Employee WHERE employee_id='{0}'""".format(
			eid
		)
		cursor.execute(query)
	


class Customer():
	def __init__(self, name, email, phone, rescoins):
		# self.customer_id=customer_id
		self.name=name
		self.email=email
		self.phone=phone
		self.rescoins=rescoins

	def insert(self):
		cursor = connection.cursor()
		query = """INSERT INTO Customer
					(name, email, phone, rescoins)
					VALUES ('{0}','{1}','{2}','{3}')""".format(
						self.name,
						self.email,
						self.phone,
						self.rescoins
					)
		cursor.execute(query)
		# self.customer_id =  #GET ORDER ID HERE FROM QUERY SOMEHOW

	def update(self):
		cursor = connection.cursor()
		query = """UPDATE TABLE Customer SET
					name='{0}',
					email='{1}',
					phone='{2}',
					rescoins='{3}'
					WHERE customer_id={4};
				""".format(
					self.name,
					self.email,
					self.phone,
					self.rescoins,
					self.customer_id
				)
		cursor.execute(query)

	@staticmethod
	def find(cid):
		cursor = connection.cursor()
		query = """SELECT customer_id, name, email, phone, rescoins
					FROM Customer WHERE customer_id='{0}'
				""".format(
					cid
				)
		cursor.execute(query)
		rows = cursor.fetchall()
		Customer = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4])
			o.customer_id = row[0]
			Customer.append(o)
		return Customer[0]

	@staticmethod
	def find_all():
		cursor = connection.cursor()
		query = """SELECT customer_id, name, email, phone, rescoins
				   FROM Customer
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		Customer = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4])
			o.customer_id = row[0]
			Customer.append(o)
		return Customer

	@staticmethod
	def delete(cid):
		cursor = connection.cursor()
		query = """DELETE FROM Customer WHERE customer_id='{0}'""".format(
			cid
		)
		cursor.execute(query)

