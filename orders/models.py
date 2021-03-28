from django.db import connection

# DATETIME MIGHT CAUSE PROBLEMS! BEWARE!!
# Create your models here.
class Order():
	def __init__(self, order_time, order_status, order_type, customer_id, address_id, payment_method, total_bill, rating, feedback):
		self.order_id=-1
		self.order_time=order_time
		self.order_status=order_status
		self.order_type=order_type
		self.customer_id=customer_id
		self.address_id=address_id
		self.payment_method=payment_method
		self.total_bill=total_bill
		self.rating=rating
		self.feedback=feedback

	def insert(self):
		cursor = connection.cursor()
		query = """INSERT INTO orders
					(order_time, order_status, order_type, customer_id,
					address_id, payment_method, total_bill, rating, feedback)
					VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(
						self.order_time,
						self.order_status,
						self.order_type,
						self.customer_id,
						self.address_id,
						self.payment_method,
						self.total_bill,
						self.rating,
						self.feedback
					)
		cursor.execute(query)

		query = """SELECT LAST_INSERT_ID();"""
		cursor.execute(query)
		rows = cursor.fetchall()
		for row in rows:
			self.order_id = row[0]
		# self.order_id =  #GET ORDER ID HERE FROM QUERY SOMEHOW

	def update(self):
		cursor = connection.cursor()
		query = """UPDATE TABLE orders SET
					order_time='{0}',
					order_status='{1}',
					order_type='{2}',
					customer_id='{3}',
					address_id='{4}',
					payment_method='{5}',
					total_bill='{6}',
					rating='{7}',
					feedback='{8}'
					WHERE order_id={9};
				""".format(
					self.order_time,
					self.order_status,
					self.order_type,
					self.customer_id,
					self.address_id,
					self.payment_method,
					self.total_bill,
					self.rating,
					self.feedback,
					self.order_id
				)
		cursor.execute(query)

	@staticmethod
	def find(oid):
		cursor = connection.cursor()
		query = """SELECT order_id, order_time, order_status, order_type, customer_id,
					address_id, payment_method, total_bill, rating, feedback
					FROM orders WHERE order_id='{0}'
				""".format(
					oid
				)
		cursor.execute(query)
		rows = cursor.fetchall()
		orders = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
			o.order_id = row[0]
			orders.append(o)
		return orders[0]

	@staticmethod
	def find_all():
		cursor = connection.cursor()
		query = """SELECT order_id, order_time, order_status, order_type, customer_id,
					address_id, payment_method, total_bill, rating, feedback
					FROM orders
				"""
		cursor.execute(query)
		rows = cursor.fetchall()
		orders = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
			o.order_id = row[0]
			orders.append(o)
		return orders

	@staticmethod
	def delete(oid):
		cursor = connection.cursor()
		query = """DELETE FROM orders WHERE order_id='{0}'""".format(
			oid
		)
		cursor.execute(query)

