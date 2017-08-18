class Cart(object):
    def __init__(self):
        self.total = 0
        self.items = {}
        self.db = []

    def add_item(self, item_name, quantity):

        #self.items.clear()
        #if item_name not in self.items.keys():
        self.items = {"parent": item_name, "quantity": quantity, "type": 'sku'}
        self.db.append(self.items)

    def delete_item(self, item):
        for it in self.db:
            if it.get("parent") == item:
                self.db.remove(it)
                return "item delete"
