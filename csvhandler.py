import csv
import os
from product import Product
from arraybag import ArrayBag

FILENAME = "InventoryData.csv"


# helper class for CSV operations
class CSVHandler(object):
    # constructor
    def __init__(self, filename):
        self.input_file = filename
        self.temp_file = "InventoryTmp.csv"

    # read the CSV file
    def read_file(self):
        """return header names, inventory ArrayBag object"""
        # set inventory as empty ArrayBag object
        inventory = ArrayBag()

        # open CSV file for reading, create a reader, make Products from rows, add Products to inventory
        with open(self.input_file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            line_count = 0
            for row in reader:
                # top line >> headers
                if line_count == 0:
                    header_names = row
                    line_count += 1
                # build a product from each row
                product = Product(  row["ItemID"],
                                    row["Manufacturer"],
                                    row["Item"],
                                    row["UnitCost"],
                                    row["UnitPrice"],
                                    row["Stock"],
                                    row["SKU"])
                # add Product to inventory
                inventory.add(product)
                line_count += 1

        return header_names, inventory

    # helper method to read to internal data list from CSV file, sort data
    def update_data_from_file(self):
        # open CSV file for reading, pull headers from row 0, pull row data from other rows
        with open(self.input_file, mode="r", newline='') as csv_read_file:
            filereader = csv.reader(csv_read_file)
            linecount = 0
            headers = []
            data = []
            for row in filereader:
                if linecount == 0:
                    headers = row
                    linecount += 1
                else:
                    data.append(row)
                    linecount += 1

        # sort the data
        data.sort()

        return headers, data

    # helper method to write to the CSV file from passed-in updated headers/data list
    def update_csv_file(self, headers, data):
        # open file for writing
        with open(self.input_file, mode="w", newline='') as csv_write_file:
            filewriter = csv.writer(csv_write_file, delimiter=',')
            # write headers to CSV
            filewriter.writerow(headers)
            # write data to CSV, row by row
            for row in data:
                filewriter.writerow(row)

    # sort the CSV file by product ID
    def sort_by_product_id(self):
        # get the data from the CSV, sort it
        headers, data = self.update_data_from_file()
        # push sorted data back to CSV
        self.update_csv_file(headers, data)

    # update the CSV file based on inventory ArrayBag's current state
    def update_file_from_inventory(self, headers, inventory):
        inventory_bag = inventory
        # open CSV file for writing
        with open(self.input_file, mode="w", newline='') as csv_file:
            filewriter = csv.writer(csv_file, delimiter=",")
            # write headers to file
            filewriter.writerow(headers)
            # iterate over all products in inventory ArrayBag, writing them as rows to CSV file
            for product in inventory_bag:
                filewriter.writerow([product.item_id,
                                     product.item_manufacturer,
                                     product.item_name,
                                     product.item_cost,
                                     product.item_price,
                                     product.quantity_in_stock,
                                     product.item_sku])

    # DEPRECATED METHODS
    # add a new line with customer data to the CSV file
    # def add_product(self, product):
    #     p = product
    #     with open(self.input_file, mode="a", newline='') as csv_file:
    #         filewriter = csv.writer(csv_file, delimiter=",")
    #         filewriter.writerow([p.item_id,
    #                             p.item_manufacturer,
    #                             p.item_name,
    #                             p.item_cost,
    #                             p.item_price,
    #                             p.quantity_in_stock,
    #                             p.item_sku])
    #     # print("Product added: ", p.item_name)
    #     # print()

    # remove a customer from the CSV file
    # def remove_product(self, product):
    #     product_id_to_remove = str(product.item_id)
    #     headers, data = self.update_data_from_file()
    #
    #     for row in data:
    #         if row[0] == product_id_to_remove:
    #             data.remove(row)
    #
    #     self.update_csv_file(headers, data)

    # def update_product(self, old_product, updated_product):
    #     self.remove_product(old_product)
    #     self.add_product(updated_product)
    #     self.sort_by_product_id()