import Customer
from Customer import Customer_Order
from Customer import CFA_Menu
from matplotlib import pyplot as plt 
import numpy as np 

def generate_customer():
    menu = CFA_Menu().order_list
    order1 = Customer_Order(order = {"Deluxe Sandwich": 3, "Spicy Chicken Sandwich": 1}, menu=menu)
    order2 = Customer_Order(order = {"Spicy Chicken Sandwich": 1}, menu=menu)
    order3 = Customer_Order(order = {"Chicken Sandwich": 2,"Spicy Chicken Sandwich": 1}, menu=menu)
    order4 = Customer_Order(order = {"Spicy Deluxe Sandwich": 5,"Spicy Chicken Sandwich": 1}, menu=menu)
    order5 = Customer_Order(order = {"Grilled Chicken Sandwich": 7}, menu=menu)
    order6 = Customer_Order(order = {"Grilled Chicken Club": 12}, menu=menu)
    order7 = Customer_Order(order = {"Chick-n-Strips": 67}, menu=menu)
    order8 = Customer_Order(order = {"Grilled Cool Wrap": 55}, menu=menu)
    order9 = Customer_Order(order = {"Grilled Nuggets": 34}, menu=menu)
    order10 = Customer_Order(order = {"Sriracha Sauce": 300}, menu=menu)
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
    customer1 = Customer.Customer(face_id = 0, all_past_orders= orderList, menu_length=len(menu))
    return customer1


def bar_chart(customer, menu):
    # subplot1: top 10 last 10 likelihoods
    index = customer.get_top10_last10()
    # print(menu[])
    # print(np.nonzero(index))
    # print(type(index))
    top10last10_menu_item = []
    top10last10_prob = []
    for ind in index:
        top10last10_menu_item.append(menu[ind])
        top10last10_prob.append(customer.item_ordering_likelihood[ind] * 100)
    y_pos = np.arange(len(top10last10_menu_item))

    fig = plt.bar(y_pos, top10last10_prob, align='center', alpha=0.5)
    plt.xticks(y_pos, top10last10_menu_item, rotation=15)
    plt.autoscale()
    plt.ylabel('Ordering Probability')
    plt.title('top 10 past 10')

    # subplot2: top 10 most likely item to order
    # subplot3: top 10 number of items ordered


    # title = ['top 10 past 10', 'top 10 all time', 'top item amount', 'empty stat']
    # axes = []
    # for i in range(1,5,1):
    #     ax = plt.subplot(2, 2, i, title=title[i-1], autoscaley_on=True)
    #     axes.append(ax)

    plt.show()

if __name__ == "__main__":
    menu = CFA_Menu().order_list
    cus1 = generate_customer()
    bar_chart(cus1, menu)