import numpy as np
import pandas as pd 

class CFA_Menu():
    def __init__(self):
        self.order_list = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich", 
            "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets", 
            "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis", 
            "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit", 
            "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns", "Greek Yogurt Parfait", 
            "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito", 
            "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin", 
            "Sausage, Egg & Cheese Muffin", "Cobb Salad", "Waffel Potato Fries", "Side Salad", 
            "Chicken Noodle Soup", "Chicken Tortilla Soup", "Superfood Side", "Buddy's Apple Sauce", 
            "Carrot Raisin Salad", "Chicken Salad", "Cole Slaw", "Cornbread", "Waffle Potato Chips", 
            "Nugget Kid's Meal", "Chick-n-Strips Kid's Meal", "Grilled Nuggets Kid's Meal", 
            "Chocolate Milkshake", "Cookies & Cream Milkshake", "Strawberry Milkshake", 
            "Vanilla Milkshake", "Frosted Coffee", "Frosted Lemonade", "Chocolate Chunk Cookie",
            "Icedream Cone", "Frosted Key Lime", "Freshly-Brewed Iced Tea Sweetened", "Lemonade", 
            "Coca-Cola", "Dr Pepper", "DASANI Bottled Water", "Honest Kids Apple Juice", 
            "Simply Orange", "1% Chocolate Milk", "1% White Milk", "Coffee", "Iced Coffee", 
            "Gallon Beverages", "Chick-fil-A Diet Lemonade", "Freshly-Brewed Iced Tea Unsweetened",
            "Chick-fil-A Sauce", "Polynesian Sauce", "Honey Mustard Sauce", "Garden Herb Ranch Sauce",
            "Zesty Buffalo Sauce", "Barbeque Sauce", "Sriracha Sauce"]
class Customer_Order():
    def __init__(self, order = dict(), menu = CFA_Menu):
        # {"menu item" : (how many)}
        self.order = dict()
        # [0 0 0 0 1 0 0 0] corresponding to the (current = 71) menu items
        self.order_item_check_array = None
        # [1 0 3 5 0 0 0 0]
        self.order_item_amount_array = None
        # add order if not empty
        if (bool(order)):
            self.order_item_check_array = np.zeros(len(menu))
            self.order_item_amount_array = np.zeros(len(menu))                
            for key, value in order.items():
                if (key not in menu):
                    raise ValueError("menu item not found")
                else:
                    self.order[key] = value
                    self.order_item_amount_array[menu.index(key)] = value
                    self.order_item_check_array[menu.index(key)] = 1

    def __str__(self):
        return ("".join(str(key) + ": " + str(value) for key, value in self.order.items()))
class Customer():
    def __init__(self, all_past_orders=[], face_id=None, menu_length=0):
        self.face_id = face_id
        self.info = pd.DataFrame(dtype=object)
        self.menu_length = menu_length

        # [{"Chicken Sandwich" : (how many)}, {}, {}]
        self.all_past_orders = all_past_orders
        self.total_order_number = len(self.all_past_orders)
        self.item_ordering_likelihood_check = np.zeros(self.menu_length)
        # [3% 10% 0%]
        self.item_ordering_likelihood = np.zeros(self.menu_length)
        # [33 44 55 0 7 1]
        self.item_amount = np.zeros(self.menu_length)

        for order in self.all_past_orders:
            self.item_ordering_likelihood_check += order.order_item_check_array
            self.item_amount += order.order_item_amount_array
        self.item_ordering_likelihood = self.item_ordering_likelihood_check / self.total_order_number
                 
        

    def add(self, order = Customer_Order):
        # add order
        self.all_past_orders.append(order)
        self.total_order_number += 1
        self.item_amount += order.order_item_amount_array
        self.item_ordering_likelihood_check += order.order_item_check_array
        self.item_ordering_likelihood = self.item_ordering_likelihood_check / self.total_order_number
    
    def __str__(self):
        item_likelihoods = np.around(self.item_ordering_likelihood, decimals=2)
        return("faceID: {}\norder percentage: {}\ntotal item ordered: {}".format(self.face_id, item_likelihoods, self.item_amount))


if __name__ == "__main__":
    # customerTest = Customer()
    menu = CFA_Menu().order_list
    order1 = Customer_Order(order = {"Deluxe Sandwich": 3}, menu=menu)
    order2 = Customer_Order(order = {"Deluxe Sandwich": 3}, menu=menu)
    order3 = Customer_Order(order = {"Chicken Sandwich": 3}, menu=menu)
    orderList = []
    orderList.append(order1)
    orderList.append(order2)
    orderList.append(order3)

    customer1 = Customer(face_id = 0, all_past_orders= orderList, menu_length=len(menu))

    # print(order2)

    print(customer1)
    customer1.add(order1)
    print(customer1)
