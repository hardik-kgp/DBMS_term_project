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
			o = Employee(row[1], row[2], row[3])
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
			o = Employee(row[1], row[2], row[3])
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


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	customer_id = models.IntegerField()

	def __str__(self):
		return self.user.username
