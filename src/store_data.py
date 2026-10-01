"""Local data for the Corner Store Assistant exercise. Prices are in AED."""

INVENTORY = {
    # Dairy and eggs
    "milk":            {"category": "dairy",     "unit": "bottle", "price": 7.00,  "stock": 12},
    "eggs":            {"category": "dairy",     "unit": "carton", "price": 12.00, "stock": 8},
    "butter":          {"category": "dairy",     "unit": "pack",   "price": 11.50, "stock": 6},
    "cheddar cheese":  {"category": "dairy",     "unit": "pack",   "price": 14.00, "stock": 9},
    "yogurt":          {"category": "dairy",     "unit": "cup",    "price": 3.50,  "stock": 24},
    "cream":           {"category": "dairy",     "unit": "bottle", "price": 9.00,  "stock": 0},

    # Bakery
    "bread":           {"category": "bakery",    "unit": "loaf",   "price": 4.50,  "stock": 0},
    "croissant":       {"category": "bakery",    "unit": "piece",  "price": 5.00,  "stock": 15},
    "bagels":          {"category": "bakery",    "unit": "pack",   "price": 8.00,  "stock": 7},
    "tortilla wraps":  {"category": "bakery",    "unit": "pack",   "price": 6.50,  "stock": 11},

    # Fruit and vegetables
    "apples":          {"category": "produce",   "unit": "kg",     "price": 3.00,  "stock": 30},
    "bananas":         {"category": "produce",   "unit": "kg",     "price": 4.00,  "stock": 0},
    "oranges":         {"category": "produce",   "unit": "kg",     "price": 5.50,  "stock": 18},
    "tomatoes":        {"category": "produce",   "unit": "kg",     "price": 4.80,  "stock": 20},
    "cucumbers":       {"category": "produce",   "unit": "kg",     "price": 3.50,  "stock": 14},
    "potatoes":        {"category": "produce",   "unit": "kg",     "price": 2.80,  "stock": 40},
    "onions":          {"category": "produce",   "unit": "kg",     "price": 2.50,  "stock": 35},
    "lettuce":         {"category": "produce",   "unit": "piece",  "price": 4.20,  "stock": 3},

    # Pantry
    "rice":            {"category": "pantry",    "unit": "bag",    "price": 22.00, "stock": 10},
    "pasta":           {"category": "pantry",    "unit": "pack",   "price": 6.00,  "stock": 25},
    "olive oil":       {"category": "pantry",    "unit": "bottle", "price": 35.00, "stock": 4},
    "sugar":           {"category": "pantry",    "unit": "bag",    "price": 5.50,  "stock": 16},
    "salt":            {"category": "pantry",    "unit": "pack",   "price": 2.00,  "stock": 30},
    "flour":           {"category": "pantry",    "unit": "bag",    "price": 7.50,  "stock": 12},
    "honey":           {"category": "pantry",    "unit": "jar",    "price": 28.00, "stock": 5},
    "peanut butter":   {"category": "pantry",    "unit": "jar",    "price": 16.00, "stock": 8},
    "canned tuna":     {"category": "pantry",    "unit": "can",    "price": 6.50,  "stock": 22},
    "breakfast cereal": {"category": "pantry",   "unit": "box",    "price": 15.00, "stock": 0},

    # Drinks
    "coffee":          {"category": "drinks",    "unit": "pack",   "price": 25.00, "stock": 5},
    "tea bags":        {"category": "drinks",    "unit": "box",    "price": 10.00, "stock": 13},
    "orange juice":    {"category": "drinks",    "unit": "bottle", "price": 9.50,  "stock": 10},
    "sparkling water": {"category": "drinks",    "unit": "bottle", "price": 3.00,  "stock": 48},
    "cola":            {"category": "drinks",    "unit": "can",    "price": 2.50,  "stock": 60},
    "energy drink":    {"category": "drinks",    "unit": "can",    "price": 7.00,  "stock": 2},

    # Snacks
    "potato chips":    {"category": "snacks",    "unit": "bag",    "price": 5.00,  "stock": 28},
    "chocolate bar":   {"category": "snacks",    "unit": "bar",    "price": 4.00,  "stock": 45},
    "cookies":         {"category": "snacks",    "unit": "pack",   "price": 6.00,  "stock": 19},
    "salted nuts":     {"category": "snacks",    "unit": "bag",    "price": 12.00, "stock": 7},
    "granola bars":    {"category": "snacks",    "unit": "box",    "price": 14.50, "stock": 9},

    # Household
    "dish soap":       {"category": "household", "unit": "bottle", "price": 9.00,  "stock": 15},
    "paper towels":    {"category": "household", "unit": "pack",   "price": 13.00, "stock": 20},
    "laundry detergent": {"category": "household", "unit": "bottle", "price": 32.00, "stock": 6},
    "trash bags":      {"category": "household", "unit": "roll",   "price": 8.50,  "stock": 0},
}

# Discount codes for the optional apply_discount experiment.
# percent: percentage taken off the total
# min_total: minimum basket total (AED) required to use the code
# active: False means the code has been disabled by the store
DISCOUNT_CODES = {
    "SAVE10":   {"percent": 10, "min_total": 0,   "active": True},
    "WELCOME5": {"percent": 5,  "min_total": 0,   "active": True},
    "BIG20":    {"percent": 20, "min_total": 200, "active": True},
    "WEEKEND15": {"percent": 15, "min_total": 50, "active": True},
    "FRESH12":  {"percent": 12, "min_total": 30,  "active": True},
    "SUMMER25": {"percent": 25, "min_total": 100, "active": False},
}