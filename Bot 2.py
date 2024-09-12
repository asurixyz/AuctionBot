from Strategy import StrategyBase
import numpy as np

class AdaptiveAuctionBot(StrategyBase):
    def __init__(self):
        super().__init__()
        self.round_count = 0
        self.win_count = 0
        self.total_profit = 0
        self.bid_history = []
        self.value_history = []
        self.aggressiveness = 1.0  # Start at neutral aggressiveness
        self.last_winning_bid = 0
        self.last_round_profit = 0

    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        self.round_count += 1
        self.value_history.append(current_value)

        # Update last winning bid
        if previous_winners:
            self.last_winning_bid = max(previous_winners)

        # Determine optimal bid based on history and capital
        optimal_bid = self.calculate_optimal_bid(current_value, capital, num_bidders)
        
        # Apply risk management and aggressiveness control
        adjusted_bid = self.adjust_bid_for_market(optimal_bid, previous_winners, previous_second_highest_bids)
        final_bid = self.apply_risk_management(adjusted_bid, capital, current_value)

        self.bid_history.append(final_bid)
        return final_bid

    def calculate_optimal_bid(self, current_value, capital, num_bidders):
        # Use historical values to estimate the optimal bid
        if len(self.value_history) < 5:
            return min(capital, current_value * 0.1)  # Safe default if insufficient history

        mean_value = np.mean(self.value_history[-5:])  # Mean of last 5 values
        std_value = np.std(self.value_history[-5:])    # Standard deviation of last 5 values
        
        expected_bid = mean_value + std_value * self.aggressiveness  # Bid above the mean adjusted for volatility
        return min(expected_bid, current_value, capital)

    def adjust_bid_for_market(self, bid, previous_winners, previous_second_highest_bids):
        if not previous_winners:
            return bid

        recent_winners = previous_winners[-5:] if len(previous_winners) > 5 else previous_winners
        recent_second_highest = previous_second_highest_bids[-5:] if len(previous_second_highest_bids) > 5 else previous_second_highest_bids

        avg_winner = np.mean(recent_winners)
        avg_second = np.mean(recent_second_highest)

        # Adjust bid based on market behavior
        if bid < avg_winner:
            bid = min(avg_winner + (avg_winner - avg_second) * 0.5, bid * 1.5)  # Aggressive adjustment
        return bid

    def apply_risk_management(self, bid, capital, current_value):
        # Adjust bid based on remaining capital
        if capital < 100:
            return min(bid, capital * 0.5, current_value)  # Conservative when low on capital
        elif capital > 1000:
            return min(max(bid, self.last_winning_bid * 1.1), capital * 0.4, current_value)  # More aggressive with high capital
        return min(max(bid, self.last_winning_bid), capital * 0.85, current_value)  # Default behavior

    def post_round_update(self, won, capital_change):
        if won:
            self.win_count += 1
            self.total_profit += capital_change
            self.last_round_profit = capital_change  # Track last round's profit for performance analysis

        # Adjust aggressiveness based on recent performance
        if self.round_count % 20 == 0:
            win_rate = self.win_count / self.round_count
            if win_rate < 0.3:
                self.aggressiveness = min(self.aggressiveness * 1.1, 2.0)  # Increase aggressiveness if losing too often
            elif win_rate > 0.5:
                self.aggressiveness = max(self.aggressiveness * 0.9, 1.0)  # Decrease if winning too frequently