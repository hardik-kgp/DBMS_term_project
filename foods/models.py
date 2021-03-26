from django.db import connection

to_bool = lambda x:x==b'\x01'
to_int = lambda x: 1 if x else 0
# Create your models here.
class food_item():
    def __init__(self, name, item_type, price, is_veg, availability, is_combo):
        self.food_id=-1
        self.name=name
        self.type=item_type
        self.price=price
        self.is_veg=bool(is_veg)
        self.availability=bool(availability)
        self.is_combo=bool(is_combo)

    def insert(self):
        cursor = connection.cursor()
        query = """INSERT INTO food_item
                    (name, type, price, is_veg, availability, is_combo)
                    VALUES ('{0}','{1}','{2}',b'{3}',b'{4}',b'{5}')""".format(
                        self.name,
                        self.type,
                        self.price,
                        to_int(self.is_veg),
                        to_int(self.availability),
                        to_int(self.is_combo)
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
        self.filter_for_db()
        query = """UPDATE TABLE food_item SET
                    name='{0}',
                    type='{1}',
                    price='{2}',
                    is_veg=b'{3}',
                    availability=b'{4}',
                    is_combo=b'{5}',
                    WHERE food_id='{6}';
                """.format(
                    self.name,
                    self.type,
                    self.price,
                    to_int(self.is_veg),
                    to_int(self.availability),
                    to_int(self.is_combo),
                    self.food_id
                )
        cursor.execute(query)

    @staticmethod
    def find(food_id):
        cursor = connection.cursor()
        print("finding food id: ", food_id)
        query = """SELECT food_id, name, type, price, is_veg, availability, is_combo
                    FROM food_item WHERE food_id='{0}'
                """.format(
                    food_id
                )
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
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
            o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
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
            o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
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
            o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
            o.food_id = row[0]
            food_items.append(o)
        return food_items

    @staticmethod
    def find_combo_internals(fcid):
        cursor = connection.cursor()
        query = """SELECT fi.food_id, fi.name, fi.type, fi.price, fi.is_veg, fi.availability, fi.is_combo, fc.quantity
                   FROM food_item fi, food_combos fc
                   WHERE fc.combo_food_id = '{0}' AND fc.food_id = fi.food_id
                """.format(
                    fcid
                )
        cursor.execute(query)
        rows = cursor.fetchall()
        food_items = []
        for row in rows:
            o = food_item(row[1],row[2],row[3],to_bool(row[4]), to_bool(row[5]), to_bool(row[6]))
            o.food_id = row[0]
            qty = row[7]
            food_items.append((o,qty))
        return food_items

    @staticmethod
    def delete(food_id):
        cursor = connection.cursor()
        query = """DELETE FROM food_item WHERE food_id='{0}'""".format(
            food_id
        )
        cursor.execute(query)
        

    @staticmethod
    
    # TODO find the trending food names
    def find_max_occuring_food_today():
        pass
    
    def find_max_occuring_food_this_month():
        pass
    
    def find_max_occuring_food_this_year():
        pass
    
    
        
        
