import json
import random

"""
Customer face ID

    current customer orders [bool]
        TODO All items
        [Chick Biscuit, Minis, Egg White Grill, Bacon Egg And Cheese Biscuit, Sausage Egg and Cheese Biscuit]
        Top 10 (Currently Using)
        [Spicy Deluxe Sandwich, Chicken Biscuit, Chick-N-Strips, Hash Browns, Lemonade, Iced Tea, Chick Sandwich,
        Chick Nuggets, Waffle Fries, Soft Drink]


"""


Total_Customers = 10
Total_Items = 10

for i in range(Total_Customers):
    customer_id = i
    current_order = []
    order_percentage = []
    for num in range(Total_Items):
        order = bool(random.getrandbits(1))
        current_order.append(order)
        order_percentage.append(random.uniform(0, 1))
    with open('customer{}.json'.format(i), 'w') as outfile:
        json.dump({"CustomerID: {}".format(i): ["current_orders: {}".format(current_order), 
        "order_percentage: {}".format(order_percentage)]}, outfile)
    print(json.dumps({"CustomerID: {}".format(i): ["current_orders: {}".format(current_order), 
        "order_percentage: {}".format(order_percentage)]},indent=4, separators=(',', ': ')))
            
        
