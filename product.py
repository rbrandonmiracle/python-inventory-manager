# define Product object for holding, manipulating, and passing along product data
class Product(object):
    # constructor
    def __init__(self, id, manufacturer, name, cost, price, stock, sku):
        # object attributes
        self.item_id = id
        self.item_manufacturer = manufacturer
        self.item_name = name
        self.item_cost = float(cost)
        self.item_price = float(price)
        self.quantity_in_stock = int(stock)
        self.item_sku = sku

    # string representation of product object
    def __repr__(self):
        item_string = str("{}: {}".format(self.item_id, self.item_name))
        return item_string
