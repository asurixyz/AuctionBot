from Strategy import StrategyBase

class UserStrategy(StrategyBase):
  
    def make_bid(self, current_value, previous_winners,previous_second_highest_bids,capital,num_bidders):
        bidf = (num_bidders-1)/num_bidders
        bid = bidf * current_value
        bid = max(0,min(capital,bid))
        return bid