from django.db import connection

# Create your models here.
class food_item():
    def __init__(self, name, item_type, price, is_veg, availability, is_combo):
        self.food_id=-1
        self.name=name
        self.type=item_type
        self.price=price
        self.is_veg=is_veg
        self.availability=availability
        self.is_combo=is_combo

    def insert(self):
        cursor = connection.cursor()
        query = """INSERT INTO food_item
                    (name, type, price, is_veg, availability, is_combo)
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')""".format(
                        self.name,
                        self.type,
                        self.price,
                        self.is_veg,
                        self.availability,
                        self.is_combo
                    )
        cursor.execute(query)

        # setting food_if for newly created item
        query = """SELECT LAST_INSERT_ID();"""
        cursor.execute(query)

        rows = cursor.fetchall()
        for row in rows:
            self.food_id = row[0]



    def update(self):
        cursor = connection.cursor()
        query = """UPDATE TABLE food_item SET
                    name='{0}',
                    type='{1}',
                    price='{2}',
                    is_veg='{3}',
                    availability='{4}',
                    is_combo='{5}',
                    WHERE food_id={6};
                """.format(
                    self.name,
                    self.type,
                    self.price,
                    self.is_veg,
                    self.availability,
                    self.is_combo,
                    self.food_id
                )
        cursor.execute(query)

    @staticmethod
    def find(food_id):
        cursor = connection.cursor()
        query = """SELECT food_id, name, type, price, is_veg, availability, is_combo
                    FROM food_item WHERE food_id='{0}'
                """.format(
                    food_id
                )
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],row[4], row[5], row[6])
            o.food_id = row[0]
            food_items.append(o)
        return food_items[0]

    @staticmethod
    def find_all():
        cursor = connection.cursor()
        query = """SELECT food_id, name, type, price, is_veg, availability, is_combo
                   FROM food_item
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],row[4], row[5], row[6])
            o.food_id = row[0]
            food_items.append(o)
        return food_items
    
    @staticmethod
    def find_all_non_combos():
        cursor = connection.cursor()
        query = """SELECT food_id, name, type, price, is_veg, availability, is_combo
                   FROM food_item
                   WHERE is_combo = 0
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],row[4], row[5], row[6])
            o.food_id = row[0]
            food_items.append(o)
        return food_items
    
    @staticmethod
    def find_all_combos():
        cursor = connection.cursor()
        query = """SELECT food_id, name, type, price, is_veg, availability, is_combo
                   FROM food_item
                   WHERE is_combo = 1
                """
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],row[4], row[5], row[6])
            o.food_id = row[0]
            food_items.append(o)
        return food_items

    @staticmethod
    def delete(food_id):
        cursor = connection.cursor()
        query = """DELETE FROM food_item WHERE food_id='{0}'""".format(
            food_id
        )
        cursor.execute(query)
