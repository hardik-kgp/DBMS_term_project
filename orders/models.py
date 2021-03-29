from django.db import connection
from foods.models import food_item

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
					VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7},'{8}')""".format(
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

	@staticmethod
	def insert_order_items(oid, ordered_items):
		cursor = connection.cursor()
		for item, count in ordered_items.items():
			f = food_item.find(item)
			query = """INSERT INTO order_items values ('{0}','{1}', '{2}')""".format(oid, f.food_id, count)
			cursor.execute(query)

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
	
	@staticmethod
	def find_orders_of_customer(cid):
		cursor = connection.cursor()
		query = """ SELECT * FROM orders WHERE orders.customer_id = {0}""".format(cid)
		cursor.execute(query)
		rows = cursor.fetchall()
		orders = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
			o.order_id = row[0]
			orders.append(o)
		return orders

	@staticmethod
	def find_orders_by_employee(eid):
		cursor = connection.cursor()
		query = """ SELECT * FROM orders 
					WHERE orders.order_id IN (SELECT order_id 
												FROM order_employee oe
												WHERE oe.employee_id = '{0}')""".format(eid)
		cursor.execute(query)
		rows = cursor.fetchall()
		orders = []
		for row in rows:
			o = Order(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
			o.order_id = row[0]
			orders.append(o)
		return orders

	@staticmethod
	def find_order_items(oid):
		cursor = connection.cursor()
		query = """ SELECT fi.food_id, fi.name, fi.type, fi.price, fi.is_veg, fi.availability, fi.is_combo, oi.quantity
						FROM food_item fi, order_items oi
						WHERE fi.food_id=oi.food_id AND order_id = '{0}')""".format(eid)
		cursor.execute(query)
		rows = cursor.fetchall()
		food_items = []
		for row in rows:
			o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
			o.food_id = row[0]
			food_items.append((o, row[7]))
		return food_items

