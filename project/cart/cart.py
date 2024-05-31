from quiz.models import product
from django.contrib import messages

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        
		# If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
		# Make sure cart is available on all pages of site
        self.cart = cart
        
    def add(self, product):
        product_id = str(product.id)
        # product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price' : str(product.pCost)}
            # self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        #u1qi1htfdqf6rl53pz8i525mgebhwk73
    
    
    def __len__(self):
        # print(self.cart)
        return len(self.cart)
    
    
    def get_prods(self):
        # get name from cart 
        product_ids = self.cart.keys()
        # use name to lookup products in database model    
        products = product.objects.filter(id__in=product_ids)
        
        return products
    

    # def get_quants(self):
    #     quantities = self.cart
    #     return quantities
    
    def delete(self, product):
        product_id = str(product)
        
        # delete from cart
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
    
    def cart_total(self, item_amount):
		# Get product IDS
        product_ids = self.cart.keys()
		# lookup those keys in our products database model
        products = product.objects.filter(id__in=product_ids)
		# Get quantities
        quantities = self.cart
		# Start counting at 0
        total = 0
        item_amount_respectively = item_amount #[1, 2, 3]
        
        new_dict = dict(zip(quantities.keys(), item_amount_respectively))
        
        for key, amount in new_dict.items():
			# Convert key string into into so we can do math
            key = int(key)
            for Product in products:
                if Product.id == key:
                    total = total + (Product.pCost * amount)
        return total
    
    def clear_items(self):
        self.cart.clear()