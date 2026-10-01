"""Local data for the Corner Store Assistant exercise. Prices are in AED."""

INVENTORY = {
    "milk":   {"price": 7.00,  "stock": 12},
    "bread":  {"price": 4.50,  "stock": 0},
    "eggs":   {"price": 12.00, "stock": 8},
    "apples": {"price": 3.00,  "stock": 30},
    "coffee": {"price": 25.00, "stock": 5},
}

# Only needed for the optional apply_discount experiment (percentage off).
DISCOUNT_CODES = {
    "SAVE10": 10,
}
