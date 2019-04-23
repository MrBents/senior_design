import numpy as np
import pandas as pd 
# import Audio_clean

class CFA_Menu():
    def __init__(self):
        self.order_list = ["Chicken Sandwich", "Deluxe Sandwich", "Spicy Chicken Sandwich", 
            "Spicy Deluxe Sandwich", "Grilled Chicken Sandwich", "Grilled Chicken Club", "Nuggets", 
            "Chick-n-Strips", "Grilled Cool Wrap", "Grilled Nuggets", "Chicken Biscuit", "Chick-n-Minis", 
            "Egg White Grill", "Bacon, Egg & Cheese Biscuit", "Sausage, Egg & Cheese Biscuit", 
            "Buttered Biscuit", "Sunflower Multigrain Bagel", "Hash Browns", "Greek Yogurt Parfait", 
            "Fruit Cup", "Chicken, Egg & Cheese Bagel", "Hash Brown Scramble Burrito", 
            "Hash Brown Scramble Bowl", "English Muffin", "Bacon, Egg & Cheese Muffin", 
            "Sausage, Egg & Cheese Muffin", "Cobb Salad", "Waffle Potato Fries", "Side Salad", 
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
        a = ("".join(str(key) + ": " + str(value) + ", " for key, value in self.order.items()))
        return a 
class Customer():
    def __init__(self, all_past_orders=[], face_id=None, menu_length=0, ethnicity=None, gender = None, age = None):
        self.face_id = face_id
        self.ethnicity = ethnicity
        self.age = age 
        self.gender = gender
        
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
    
    def get_top10_last10(self):
        ''' 
        geth the top 10 order item of the last 10 order
        :return: array of indices of the top 10 items
        '''
        top10 = []
        top10_check = np.empty(self.menu_length)
        if(len(self.all_past_orders) < 10):
            for order in self.all_past_orders:
                top10_check += order.order_item_check_array
        else:
            for order in self.all_past_orders[-10:]:
                top10_check += order.order_item_check_array
        ind = np.argpartition(top10_check, -10)[-10:]
        return ind

        
    def get_top10_all_time(self):
        ''' 
        geth the top 10 order item of all time
        :return: array of indices of the top 10 items
        '''
        top10_check = np.empty(self.menu_length)
        for order in self.all_past_orders:
            top10_check += order.order_item_check_array
        ind = np.argpartition(top10_check, -10)[-10:]
        return ind
        
    
    def __str__(self):
        # item_likelihoods = np.around(self.item_ordering_likelihood, decimals=2)
        # return("faceID: {}\norder percentage: {}\ntotal item ordered: {}".format(self.face_id, item_likelihoods, self.item_amount))
        # temp = None
        # for order in self.all_past_orders:
        #     temp = (order)
        return("faceID: {}\n".format(self.face_id, temp))
        # return("faceID: {}\nethnicity: {}\ngender: {}\n".format(self.face_id, self.ethnicity, self.gender))
        

def init_customer():
    menu = CFA_Menu().order_list
    order1 = Customer_Order(order = {"Deluxe Sandwich": 3}, menu=menu)
    order2 = Customer_Order(order = {"Spicy Chicken Sandwich": 1}, menu=menu)
    order3 = Customer_Order(order = {"Chicken Sandwich": 3}, menu=menu)
    order4 = Customer_Order(order = {"Spicy Deluxe Sandwich": 3}, menu=menu)
    order5 = Customer_Order(order = {"Grilled Chicken Sandwich": 1}, menu=menu)
    order6 = Customer_Order(order = {"Grilled Chicken Club": 3}, menu=menu)
    order7 = Customer_Order(order = {"Chick-n-Strips": 3}, menu=menu)
    order8 = Customer_Order(order = {"Grilled Cool Wrap": 3}, menu=menu)
    order9 = Customer_Order(order = {"Grilled Nuggets": 3}, menu=menu)
    order10 = Customer_Order(order = {"Chicken Biscuit": 3}, menu=menu)
    orderList = []
    orderList.append(order1)
    orderList.append(order2)
    orderList.append(order3)
    orderList.append(order4)
    orderList.append(order5)
    orderList.append(order6)
    orderList.append(order7)
    orderList.append(order8)
    orderList.append(order9)
    orderList.append(order10)

    customer1 = Customer(face_id = 0, all_past_orders= orderList, menu_length=len(menu))
    print(customer1)
    customer1.add(order1)

    # print top 10
    ind = customer1.get_top10_last10()
    print((ind))
    for x in np.nditer(ind):
        print(menu[x])

    return customer1

if __name__ == "__main__":
    menu = CFA_Menu().order_list
    # actual_order = []
    # order = Audio_clean.Audio.getOrder('Can I get three number two meal with four cookies and cream milkshake and a chicken biscuit please')
    # order = Customer_Order(order, menu=menu)
    # actual_order.append(order)
    # print(Customer(all_past_orders=actual_order, menu_length=len(menu)))
