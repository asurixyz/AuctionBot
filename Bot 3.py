from Strategy import StrategyBase
import numpy as np

class Variant3AdaptiveStrategy(StrategyBase):
    def __init__(self):
        super().__init__()
        self.round_count = 0
        self.win_count = 0
        self.second_place_count = 0
        self.total_profit = 0
        self.aggressiveness_factor = 1.0
        self.value_history = []

    def make_bid(self, current_value, previous_winners, previous_second_highest_bids, capital, num_bidders):
        self.round_count += 1
        self.value_history.append(current_value)
        # Estimate the expected maximum value (X)
        estimated_X = self.estimate_max_value(num_bidders)
        # Calculate the standard deviation of the distribution
        sigma = 100 * ((num_bidders / ((num_bidders + 1)**2 * (num_bidders + 2)))**0.5)
        # Determine the bidding factor (theta) based on the current value and market conditions
        theta = self.determine_theta(current_value, estimated_X, sigma, previous_winners, previous_second_highest_bids)
        # Calculate the bid
        bid = theta * max(estimated_X, current_value)
        # Apply risk management
        bid = self.apply_risk_management(bid, capital, estimated_X)
        return bid

    def estimate_max_value(self, num_bidders):
        theoretical_max = 100 * num_bidders / (num_bidders + 1)
        if len(self.value_history) > 20:
            observed_max = np.max(self.value_history[-20:])
            return max(theoretical_max, observed_max) * self.aggressiveness_factor
        return theoretical_max * self.aggressiveness_factor

    def determine_theta(self, current_value, estimated_X, sigma, previous_winners, previous_second_highest_bids):
        if current_value > estimated_X + sigma:
            return 0.99  # Very high value, bid aggressively
        elif estimated_X <= current_value <= estimated_X + sigma:
            return 0.98  # High value, bid confidently
        elif estimated_X - sigma <= current_value < estimated_X:
            return 0.90  # Mid-range value, bid cautiously
        else:
            # Low value, bid very cautiously or not at all
            if previous_winners and previous_second_highest_bids:
                avg_gap = np.mean(np.array(previous_winners) - np.array(previous_second_highest_bids))
                if avg_gap > sigma:
                    return 0  # High risk of being second, don't bid
            return 0.85  # Low value, bid conservatively

    def apply_risk_management(self, bid, capital, estimated_X):
        if capital < 200:
            return min(bid * 0.8, capital * 0.4)  # Very conservative when low on capital
        elif capital > 1000:
            if bid > estimated_X * 0.9:
                return min(bid * 1.05, capital * 0.3)  # Slightly more aggressive for high bids with high capital
            else:
                return min(bid, capital * 0.2)  # Normal bid for low bids with high capital
        return min(bid, capital * 0.25)  # Standard risk management

    def post_round_update(self, won, capital_change):
        if won:
            self.win_count += 1
            self.total_profit += capital_change
        elif capital_change < 0:
            self.second_place_count += 1
            self.total_profit += capital_change

        # Adjust strategy based on performance
        if self.round_count % 20 == 0:
            win_rate = self.win_count / self.round_count
            second_place_rate = self.second_place_count / self.round_count

            if win_rate < 0.2 and second_place_rate < 0.1:
                self.aggressiveness_factor = min(1.1, self.aggressiveness_factor * 1.05)
            elif second_place_rate > 0.15:
                self.aggressiveness_factor = max(0.9, self.aggressiveness_factor * 0.95)
            elif win_rate > 0.3:
                self.aggressiveness_factor = max(0.95, self.aggressiveness_factor * 0.98)