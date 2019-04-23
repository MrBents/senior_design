import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db
import inspect
import Customer
from Customer import CFA_Menu

if __name__ == '__main__':
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    dbdb = firestore.client()

    order_list = [{'value': 1, 'name': "Chicken Sandwich"}, {'value': 25, 'name': "Deluxe Sandwich"}, {'value': 10, 'name': "Spicy Chicken Sandwich"}, {'value': 5, 'name': "Spicy Deluxe Sandwich"}, {'value': 5, 'name': "Grilled Chicken Sandwich"}, {'value': 3, 'name': "Grilled Chicken Club"}, {'value': 2, 'name': "Nuggets"}]
    doc_ref = dbdb.collection(u'Customer').document(u'max')
    doc_ref.set({
        u'age': 99,
        u'ethnicity': u'white',
        u'gender': u'female',
        u'inLine': True,
        u'face_id': u'max',
        u'probabilities': order_list
    })

    # for field, val in (inspect.getmembers(doc_ref)):
    #     print(field, val) 
    cus_ref = dbdb.collection(u'Customer')

    # {'item' : amount}
    # menu = CFA_Menu.order_list
    # order1 = Customer.Customer_Order(order = {"Deluxe Sandwich": 3}, menu=menu)
    # order1 = dict(order1)
    order1 = {"Deluxe Sandwich": 300, "Chicken Sandwich": 5}
    # {'item1' : 'Chickem Nuggets'...}
    va = 'sam'
    a_ref = cus_ref.where(u'face_id', u'==', u'{}'.format(va)).get()
    for a in a_ref:
        # a._reference.update({u'ethnicity': u'asdfasdf'})
        abc = (a._data['probabilities'])
        # print(type(abc))
        l = []
        for item in abc:
            if item['name'] in order1.keys():
                print(item['name'])
                # print(order1.get((item['name'])))
                item['value'] += order1.get((item['name']))
                # a._reference.update()
            l.append(item)
        a._reference.update({u'probabilities': l})

        

    # cus = cus_ref.get()
    # for doc in cus: 
    #     print(u'{} => '.format(doc.id))     
    #     print(u'{}'.format(doc.to_dict()))
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))

    # print(doc_ref._path)
    # snapshot = doc_ref.order_by_child('age').get()
    # print(snapshot)
    # ref = db.reference()
    # print(doc_ref.get())
    # print(doc_ref.get().value())
