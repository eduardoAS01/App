
class ProductService():

    @staticmethod
    def check_profit(cost_price:float,sale_price:float):

        if cost_price >= sale_price:
            return{
                "warning":True,
                "message":"Cost price is superior than sale price. You wont have profit"
            }
        
        if round((sale_price - cost_price)/cost_price * 100) < 15:
            return{
                "warning":True,
                "message":"Profit percentage below 15% thats not the best to grow"
            }

        return {"warning":False}
   