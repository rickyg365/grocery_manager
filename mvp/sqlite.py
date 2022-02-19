import os
import sqlite3

from typing import List, Dict

from models.grocery_item_model import ActiveItem, GroceryItem, grocery_model, active_model, Model

"""

"""

# Helping Functions



# Objects 

class InventoryDatabase:
    def __init__(self, custom_path="data/new_sqlite_db.db"):
        self.conn = sqlite3.connect(custom_path)
        self.cur = self.conn.cursor()

        self.tables = {
            "all_items": {
                "object": GroceryItem, 
                "model": grocery_model
            },
            "inventory": {
                "object": ActiveItem, 
                "model": active_model
            }
        }

        self.grocery_model = Model(grocery_model)
        self.active_model = Model(active_model)

        self.all_items = self.create_table("all_items")
        self.inventory = self.create_table("inventory")
        

    def __str__(self) -> str:
        txt = ""
        return txt
    
    def create_table(self, table_name: str):
        data_model = self.tables[table_name]['model']
        
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
{model_text(data_model)}
)""")

    def insert_data(self, data_object, table_name):
        # Raw Data vs python obj
        data_model = self.tables[table_name]['model'] 
        data_insert_key, data_insert_obj = parse_insert_data(data_object.raw_data(), data_model)
        
        with self.conn:
            self.cur.execute(f"INSERT INTO {table_name} VALUES ({data_insert_key})",
            data_insert_obj)

    def get_all(self, table_name) -> List[object]:
        data_obj_name = self.tables[table_name]['object']
        # Connect to table, and select all
        self.cur.execute(f'select * from {table_name}')
        results = self.cur.fetchall()

        # iterate and add to object list
        objects = []
        for result in results:
            objects.append(data_obj_name(*result))

        return objects
    
    def delete_data_point(self, key, table_name, ref_attr="id"):
        """ """
        # ref_attr = self.tables[table_name]["ref"]
        with self.conn:
            self.cur.execute(f'DELETE from {table_name} WHERE {ref_attr}=:key', {'key': key})


class FoodDatabase:
    def __init__(self, custom_path="data/new_sqlite_db.db"):
        self.conn = sqlite3.connect(custom_path)
        self.cur = self.conn.cursor()

        self.tables = {
            "recipes": {
                "object": GroceryItem, 
                "model": grocery_model
            },
            "items": {
                "object": ActiveItem, 
                "model": active_model
            },
            "recipe_ingredients": {
                "object": ActiveItem, 
                "model": active_model
            }
        }

        self.recipe_table = self.create_table("recipes")
        self.item_table = self.create_table("items")
        self.recipe_ingredient_table = self.create_table("recipe_ingredients")
    
    def __str__(self) -> str:
        txt = ""
        return txt
    
    def create_table(self, table_name: str):
        data_model = self.tables[table_name]['model']
        
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
{model_text(data_model)}
)""")

    def insert_data(self, data_object, table_name):
        # Raw Data vs python obj
        data_model = self.tables[table_name]['model'] 
        data_insert_key, data_insert_obj = parse_insert_data(data_object.raw_data(), data_model)
        
        with self.conn:
            self.cur.execute(f"INSERT INTO {table_name} VALUES ({data_insert_key})",
            data_insert_obj)

    def get_all(self, table_name) -> List[object]:
        data_obj_name = self.tables[table_name]['object']
        # Connect to table, and select all
        self.cur.execute(f'select * from {table_name}')
        results = self.cur.fetchall()

        # iterate and add to object list
        objects = []
        for result in results:
            objects.append(data_obj_name(*result))

        return objects
    
    def delete_data_point(self, key, table_name, ref_attr="id"):
        """ """
        # ref_attr = self.tables[table_name]["ref"]
        with self.conn:
            self.cur.execute(f'DELETE from {table_name} WHERE {ref_attr}=:key', {'key': key})


if __name__ == "__main__":
    new_db = InventoryDatabase()

    # 2 Tables by Default, Main and Current

    new_db.insert_data(GroceryItem(0, "name1", "desc"), "all_items")
    new_db.insert_data(ActiveItem(0, "name2", "desc"), "inventory")

    all_items = new_db.get_all("all_items")
    curr_items = new_db.get_all("inventory")

    print(f"All: \n{all_items}")
    print(f"Current: \n{curr_items}")

    new_db.delete_data_point(0, "all_items")
    new_db.delete_data_point(0, "inventory")

