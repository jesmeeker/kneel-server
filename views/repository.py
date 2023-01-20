import sqlite3
import json
from models import Order, Size, Style, Metal

DATABASE = {
    'orders': [
        {
            "id": 1,
            "metalId": 1,
            "sizeId": 1,
            "styleId": 1,
        }
    ],
    'metals': [
        {
            "id": 1,
            "metal": "Sterling Silver",
            "price": 12.42
        },
        {
            "id": 2,
            "metal": "14K Gold",
            "price": 736.4
        },
        {
            "id": 3,
            "metal": "24K Gold",
            "price": 1258.9
        },
        {
            "id": 4,
            "metal": "Platinum",
            "price": 795.45
        },
        {
            "id": 5,
            "metal": "Palladium",
            "price": 1241
        }
    ],
    'sizes': [
        {
            "id": 1,
            "carets": 0.5,
            "price": 405
        },
        {
            "id": 2,
            "carets": 0.75,
            "price": 782
        },
        {
            "id": 3,
            "carets": 1,
            "price": 1470
        },
        {
            "id": 4,
            "carets": 1.5,
            "price": 1997
        },
        {
            "id": 5,
            "carets": 2,
            "price": 3638
        }
    ],
    'styles': [
        {
            "id": 1,
            "style": "Classic",
            "price": 500
        },
        {
            "id": 2,
            "metal": "Modern",
            "price": 710
        },
        {
            "id": 3,
            "metal": "Vintage",
            "price": 965
        }
    ]
}


def all(resource):
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if resource == 'orders':
            db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id,
                m.metal metal_name,
                m.price metal_price,
                s.carets carets,
                s.price size_price,
                t.style style,
                t.price style_price
            FROM Orders o
            JOIN Metals m 
            ON m.id = o.metal_id
            JOIN Sizes s
            ON s.id = o.size_id
            JOIN Styles t
            ON t.id = o.style_id
            """)

            # Initialize an empty list to hold all animal representations
            orders = []

            # Convert rows of data into a Python list
            dataset = db_cursor.fetchall()

            # Iterate list of data returned from database
            for row in dataset:

                # Create an order instance from the current row.
                # Note that the database fields are specified in
                # exact order of the parameters defined in the
                # Order class above.
                order = Order(row['id'], row['metal_id'],
                              row['size_id'], row['style_id'])

                # Create a Location instance from the current row
                metal = Metal(row['id'], row['metal_name'], row['metal_price'])

                # Add the dictionary representation of the location to the order
                order.metal = metal.__dict__

                size = Size(
                    row['id'], row['carets'], row['size_price'])

                # # Add the dictionary representation of the location to the order
                order.size = size.__dict__
                # # Add the dictionary representation of the order to the list

                # # Create a Customer instance from the current row
                style = Style(
                    row['id'], row['style'], row['style_price'])

                # # Add the dictionary representation of the location to the order
                order.style = style.__dict__
                # # Add the dictionary representation of the order to the list

                orders.append(order.__dict__)

            return orders


def retrieve(resource, id, query_params):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        if resource == 'orders' and query_params == ['']:
            db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id
            FROM Orders o
            WHERE o.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            order = Order(data['id'], data['metal_id'], data['size_id'],
                            data['style_id'])

            return order.__dict__
    # """For GET requests to a single resource"""
    # requested_resource = None
    # price = 0

    # # Iterate the ANIMALS list above. Very similar to the
    # # for..of loops you used in JavaScript.
    # for e in DATABASE[resource]:
    #     # Dictionaries in Python use [] notation to find a key
    #     # instead of the dot notation that JavaScript used.
    #     if e["id"] == id:
    #         requested_resource = e

    #     if resource == 'orders':
    #         if query_params == ['']:
    #             for i in DATABASE['metals']:
    #                 matching_metal = None
    #                 if i["id"] == requested_resource["metalId"]:
    #                     matching_metal = i
    #                     # requested_resource["metal"] = matching_metal
    #                     price += matching_metal["price"]

    #             for j in DATABASE['sizes']:
    #                 matching_size = None
    #                 if j["id"] == requested_resource["sizeId"]:
    #                     matching_size = j
    #                     # requested_resource["size"] = matching_size
    #                     price += matching_size["price"]

    #             for k in DATABASE['styles']:
    #                 matching_style = None
    #                 if k["id"] == requested_resource["styleId"]:
    #                     matching_style = k
    #                     # requested_resource["style"] = matching_style
    #                     price += matching_style["price"]

    #         elif query_params == ['_expand=metal']:
    #             for i in DATABASE['metals']:
    #                 matching_metal = None
    #                 if i["id"] == requested_resource["metalId"]:
    #                     matching_metal = i
    #                     requested_resource["metal"] = matching_metal
    #                     price += matching_metal["price"]

    #         elif query_params == ['_expand=size']:
    #             for j in DATABASE['sizes']:
    #                 matching_size = None
    #                 if j["id"] == requested_resource["sizeId"]:
    #                     matching_size = j
    #                     requested_resource["size"] = matching_size
    #                     price += matching_size["price"]

    #         elif query_params == ['_expand=style']:
    #             for k in DATABASE['styles']:
    #                 matching_style = None
    #                 if k["id"] == requested_resource["styleId"]:
    #                     matching_style = k
    #                     requested_resource["style"] = matching_style
    #                     price += matching_style["price"]

    #         else:
    #             ""

    #     requested_resource["price"] = price
    #     # del requested_resource["metalId"]
    #     # del requested_resource["sizeId"]
    #     # del requested_resource["styleId"]

    # return requested_resource


def create(resource, post_body):
    """For POST requests to a collection"""

    # Get the id value of the last animal in the list
    max_id = DATABASE[resource][-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    post_body["id"] = new_id

    # Add the animal dictionary to the list
    DATABASE[resource].append(post_body)

    # Return the dictionary with `id` property added
    return post_body


def update(resource, id, post_body):
    """For PUT requests to an individual"""

    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            # Found the animal. Update the value.
            DATABASE[resource][index] = post_body
            break


def delete(resource, id):
    """For DELETE requests to a single resource"""
    resource_index = -1

    # Iterate the ANIMALS list, but use enumerate() so that you
    # can access the index value of each item
    for index, item in enumerate(DATABASE[resource]):
        if item["id"] == id:
            # Found the animal. Store the current index.
            resource_index = index

    # If the animal was found, use pop(int) to remove it from list
    if resource_index >= 0:
        DATABASE[resource].pop(resource_index)
