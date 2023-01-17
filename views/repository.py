DATABASE = {
    'orders':
    [
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
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    requested_resource = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for e in DATABASE[resource]:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if e["id"] == id:
            requested_resource = e

            if resource == 'orders':
                for i in DATABASE['metals']:
                    matching_metal = None
                    if i["id"] == requested_resource["metalId"]:
                        matching_metal = i
                        requested_resource["metal"] = matching_metal

                for j in DATABASE['sizes']:
                    matching_size = None
                    if j["id"] == requested_resource["sizeId"]:
                        matching_size = j
                        requested_resource["size"] = matching_size

                for k in DATABASE['styles']:
                    matching_style = None
                    if k["id"] == requested_resource["styleId"]:
                        matching_style = k
                        requested_resource["style"] = matching_style

                del requested_resource["metalId"]
                del requested_resource["sizeId"]
                del requested_resource["styleId"]

    return requested_resource


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
