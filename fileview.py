from csvhandler import CSVHandler
from product import Product
from arraybag import ArrayBag


class FileView(object):

    # Constructor
    def __init__(self):
        """jump table for commands, initialize file_contents dictionary, run get_file() method"""
        # instantiate handler, including name of CSV file to use
        filename = "InventoryData.csv"
        self._handler = CSVHandler(filename)

        # initial sort of CSV file by product ID
        self._handler.sort_by_product_id()

        # define user methods
        self._methods = {}
        self._methods["1"] = self._print_file
        self._methods["2"] = self._print_product
        self._methods["3"] = self._add_product
        self._methods["4"] = self._remove_product
        self._methods["5"] = self._update_product
        self._methods["Q"] = self._quit

        # unprinted method for testing - printInventory
        self._methods["p"] = self._printInventory

        # define headers, fill inventory from CSV file
        self._headers, self._inventory = self._handler.read_file()

    # main operations
    def run(self):
        """prompt user for action they want to take, direct flow of traffic"""
        # prompt user for method to call
        while True:
            print("------------------------")
            print("1: Print Inventory")
            print("2: Print Single Product")
            print("3. Add a Product")
            print("4. Remove a Product")
            print("5. Update a Product")
            print("Q. Quit Program")
            selection = input("Choose an action (#): ").upper()
            method_chosen = self._methods.get(selection, None)

            # call necessary method
            if method_chosen is None:
                print("Unrecognized action chosen")
            else:
                method_chosen()
                if self._handler is None:
                    break

    # exit program
    def _quit(self):
        exit()

    # initialize (or re-initialize) printable table with headers
    def _initialize_table(self):
        self._table_data = [self._headers]

    # append a single line of product data to the printable table
    def _append_to_table(self, product_data):
        self._table_data.append(product_data)

    # format a string with two decimals for $$ data
    def format_two_decimals(self, string_input):
        """return a formatted XX.XX string"""
        input_string = "{input:.2f}"
        formatted_string = input_string.format(input=string_input)

        return formatted_string

    # build up a product string for adding to printable table
    def _build_product_string(self, id, manufacturer, product, cost, price, stock, sku):
        format_string = "{productID} \t {productManufacturer} \t {productName} \t " \
                        "{productCost:.2f} \t {productPrice:.2f} \t {stockQty} \t {SKU}"
        product_string = format_string.format(productID=id,
                                              productManufacturer=manufacturer,
                                              productName=product,
                                              productCost=cost,
                                              productPrice=price,
                                              stockQty=stock,
                                              SKU=sku)
        return product_string

    # access contents of CSV file
    def _get_file(self):
        """use CSVHandler class to get contents of file, store in file_contents dictionary"""
        self._handler.sort_by_product_id()
        self._headers, self._inventory = self._handler.read_file()

    # print contents of inventory (ArrayBag) object
    def _printInventory(self):
        for item in self._inventory:
            print(item)

    # test to see if a product is present in inventory, checking by product_id
    def _product_id_in_inventory(self, product_id):
        """Returns boolean of whether product is present in inventory,
        as well as that product's index within the ArrayBag object"""
        # refresh inventory from CSV file
        self._get_file()

        # initialize product_in_inventory variable to False, product_id_list to empty list, bag_index to 0
        product_in_inventory = False
        product_id_list = []
        bag_index = 0

        # iterate over products present in inventory, building up list of product_id values
        for product in self._inventory:
            product_id_list.append(product.item_id)

        # if specified product_id is in product_id_list, set boolean to True and bag_index to relevant index
        if product_id in product_id_list:
            bag_index = product_id_list.index(product_id)
            product_in_inventory = True

        return product_in_inventory, bag_index

    # print contents of entire file
    def _print_file(self):
        """refresh the file using get_file() method, iterate over file_contents to print"""
        # get (refresh) file contents, re-initialize data table
        self._get_file()
        self._initialize_table()
        print()
        print("Inventory:")

        # iterate over products in inventory
        # sort data elements into a printable table line list
        # append data to table for printing
        for product in self._inventory:
            table_line = [product.item_id,
                          product.item_manufacturer,
                          product.item_name,
                          self.format_two_decimals(product.item_cost),
                          self.format_two_decimals(product.item_price),
                          product.quantity_in_stock,
                          product.item_sku]
            self._table_data.append(table_line)

        # iterate over table data, printing in formatted rows
        for row in self._table_data:
            print("{:^12} {:^12} {:^15} {:^12} {:^14} {:^18} {:^12}".format(*row))
        print()

    # print a single line from file
    def _print_line(self, product_id):
        """prints a single line from file based on passed-in product_id"""
        self._get_file()
        self._initialize_table()

        # if the id_selection is valid, pull the contents at that bag index to a Product
        # compile a printable table line
        # append that table line to the re-initialized table and print
        product_id_in_inventory, bag_index = self._product_id_in_inventory(product_id)
        if product_id_in_inventory:
            product = self._inventory.items.__getitem__(bag_index)
            table_line = [product.item_id,
                          product.item_manufacturer,
                          product.item_name,
                          self.format_two_decimals(product.item_cost),
                          self.format_two_decimals(product.item_price),
                          product.quantity_in_stock,
                          product.item_sku]
            self._table_data.append(table_line)
            for row in self._table_data:
                print("{:^12} {:^12} {:^15} {:^12} {:^14} {:^18} {:^12}".format(*row))
        else:
            print("No product with selected ID.")
        print()

    # get product ID for printing single product, pass along to _print_line()
    def _print_product(self):
        """prompt user for product ID, access file_contents at that key if it is in file, pass id to print_line()"""
        # re-initialize table and get (refresh) file contents
        self._initialize_table()
        self._get_file()
        print()

        # get user input for which product ID to view
        id_selection = input("Which product (ID) would you like to view? ")
        print()

        # if id_selection is valid, print its details
        product_id_in_inventory, bag_index = self._product_id_in_inventory(id_selection)
        if product_id_in_inventory:
            print("Product Details:")
            self._print_line(id_selection)
        else:
            print(">>> NO PRODUCT WITH SELECTED ID <<<")
            self._print_file()
            print(">>> NO PRODUCT WITH SELECTED ID <<<")
        print()

    # add a Product to the file
    def _add_product(self):
        """prompt user for product data, create Product, send that Product to CSVHandler for adding"""
        # re-initialize table and get (refresh/sort) file contents
        self._get_file()
        self._initialize_table()
        print()

        # get last Product ID in file, increment to create next Product ID
        product_id = 0
        for product in self._inventory:
            product_id = int(product.item_id)
        product_id += 1

        # print new ID to terminal, prompt user for product data entry
        print("New Product ID: ", product_id)
        product_manufacturer = input("Product Manufacturer: ")
        product_name = input("Product Name: ")
        product_cost = input("Product Cost: ")
        product_price = input("Product Price: ")
        quantity_in_stock = input("Quantity in Stock: ")
        product_sku = str(input("Product SKU: "))

        # create a new Product from input data, add that new Product to inventory bag
        product_to_add = Product(product_id, product_manufacturer, product_name, product_cost, product_price,
                                 quantity_in_stock, product_sku)
        self._inventory.add(product_to_add)

        # push updated inventory to CSVHandler
        self._handler.update_file_from_inventory(self._headers, self._inventory)

        # print verification
        print()
        print("Product Added:")
        self._print_line(str(product_id))

    # remove a Product from CSV file based on Product ID or name
    def _remove_product(self):
        """get (refresh) file, get user input for product ID to remove, send that product to CSVHandler for removal"""
        # refresh CSV file, set handler
        self._get_file()
        print()

        # initialize product_id_in_inventory to False to open the while loop
        product_id_in_inventory = False

        # use while loop to get a product ID that is in inventory
        while not product_id_in_inventory:
            id_selection = input("Which product (ID) would you like to remove? ")
            product_id_in_inventory, bag_index = self._product_id_in_inventory(id_selection)
            # print("Selected ID not in Inventory.")
            print()

        # print verification of selected product_id
        print()
        print("Product Removed:")
        self._print_line(id_selection)

        # remove product at bag_index from inventory, push updated inventory to CSVHandler
        self._inventory.remove(self._inventory.items.__getitem__(bag_index))
        self._handler.update_file_from_inventory(self._headers, self._inventory)
        
    def _update_product(self):
        """get (refresh) file, get user input for product ID to update,
        get new updated details, send both to CSVHandler for updating"""
        # refresh CSV file, set handler
        self._get_file()
        print()

        # initialize product_id_in_inventory to False to open the while loop
        product_id_in_inventory = False

        # use while loop to get a product ID that is in file_contents keys
        while not product_id_in_inventory:
            id_selection = input("Which product (ID) would you like to update? ")
            product_id_in_inventory, bag_index = self._product_id_in_inventory(id_selection)
            print("Selected ID not in Inventory.")
            print()

        # get COPY of selected product from inventory
        # NOTE: ONLY FOR SEEING PRE-UPDATE PRODUCT INFO
        # DO NOT PASS THIS PRODUCT FOR REMOVAL FROM INVENTORY
        product = self._inventory.items.__getitem__(bag_index)
        print()
        print("Product to Update:")
        self._print_line(product.item_id)
        print()

        # prompt user for product data entry (new values for product info)
        new_id = input("Product ID: {} >> ".format(product.item_id))
        new_manufacturer = input("Product Manufacturer: {} >> ".format(product.item_manufacturer))
        new_name = input("Product Name: {} >> ".format(product.item_name))
        new_cost = input("Product Cost: {} >> ".format(product.item_cost))
        new_price = input("Product Price: {} >> ".format(product.item_price))
        new_quantity_in_stock = input("Quantity in Stock: {} >> ".format(product.quantity_in_stock))
        new_sku = str(input("Product SKU: {} >> ".format(product.item_sku)))
        updated_product = Product(new_id, new_manufacturer, new_name, new_cost, new_price,
                                 new_quantity_in_stock, new_sku)

        # remove product at selected bag_index from inventory
        self._inventory.remove(self._inventory.items.__getitem__(bag_index))

        # add updated product to inventory
        self._inventory.add(updated_product)

        # update/sort CSV File
        self._handler.update_file_from_inventory(self._headers, self._inventory)

        # print verification
        print()
        print("Updated Product: ")
        self._print_line(updated_product.item_id)
        print()


# run main
if __name__ == "__main__":
    FileView().run()
