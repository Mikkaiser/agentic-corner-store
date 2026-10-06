from store_data import INVENTORY


def get_featured_product() -> dict:
    name, product = max(INVENTORY.items(), key=lambda item: item[1]["stock"])
    return {"name": name, **product}


