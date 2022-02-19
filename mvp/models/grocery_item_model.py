import os

from typing import List, Dict, Optional
from dataclasses import dataclass, field

# Typing is for hints, dataclass does not enforce

# Sqlite3 Type Mapping

grocery_model = {
    "id": "integer",
    "name": "text",
    "description": "text",
    "brand": "text",
    "tag": "text"
}

active_model = {
    "id": "integer",
    "name": "text",
    "description": "text",
    "brand": "text",
    "tag": "text",
    "store": "text",
    "price": "integer",
    "quantity": "integer",
    "quantity_unit": "text"
}

# Python Object

@dataclass
class GroceryItem:
    id: int
    name: str
    description: str
    brand: str = field(default="")
    tags: List[str] = field(default_factory=list)

    def raw_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brand": self.brand,
            "tags": self.tags
        }


@dataclass
class ActiveItem(GroceryItem):
    store: Optional[str] = "???"
    price: float = 0.00
    quantity: int = 1
    quantity_unit: str = "of"

    def raw_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brand": self.brand,
            "tags": self.tags,
            "store": self.store,
            "price": self.price,
            "quantity": self.quantity,
            "quantity_unit": self.quantity_unit
        }


class Model:
    def __init__(self, model_data: Dict[str, str]):
        self.model_data = model_data

    def __str__(self) -> str:
        pass
    
    def model_text(self) -> str:
        """ Convert Data Model Template into Sqlite3 Language """ 
        # Split tuple into sqlite format w/ appropriate space
        parsing_function = lambda x: f"            {x[0]} {x[1]}"

        # Apply format to every key, val pair and Join with seperater
        return ",\n".join(map(parsing_function, self.model_data.items()))

    def parse_insert_data(self, raw_object_data):
        final_key = []
        final_obj = {}

        # data_object = data_object.raw_data()

        for data_key, data_type in self.model_data.items():
            # Get current value
            data_value = raw_object_data.get(data_key)

            # Create Insert Key
            final_key.append(f":{data_key}")

            # This is for general parsing but maybe define specific parsing files and move them into the Object Model File
            if data_type == 'integer':
                final_obj[data_key] = int(data_value)
            else:
                final_obj[data_key] = f"{data_value}"

        return ", ".join(final_key), final_obj


