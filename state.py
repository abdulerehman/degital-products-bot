class ProductsState:
    def __init__(self) -> None:
        self.products = []
        self.selected_product = None

    def clear(self):
        self.products = []
        self.selected_product = None
    
    def add(self, product):
        self.products.append(product)
    
    def get(self):
        return self.products

    def check(self, title):
        for product in self.products:
            if title == product['title']:
                self.selected_product = product 
                return True
        return False


class PackState:
    def __init__(self) -> None:
        self.packs = []
        self.selected_pack = None

    def clear(self):
        self.packs = []
        self.selected_pack = None

    
    def add(self, pack):
        self.packs.append(pack)
    
    def get(self):
        return self.packs

    def check(self, title):
        for pack in self.packs:
            if title == pack['title']:
                self.selected_pack = pack 
                return True
        return False



product_state = ProductsState()
pack_state = PackState()