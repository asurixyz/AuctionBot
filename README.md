# Auction Bot Competition

## Overview
This project simulates a multi-round bidding game where trading bots compete against each other to maximize profit. The competition is designed to challenge participants to develop effective bidding strategies in various auction scenarios.

## Game Setup
- **Number of Players**: n (each player is a bot developed by participants)
- **Number of Rounds**: t (~10^3)
- **Initial Condition**: At the start of each round, player i is assigned a value x_i, randomly drawn from a predefined distribution
- **Maximum Bid Value**: 100
- **Starting Capital**: Variable

## Gameplay
1. Each player receives a value x_i at the beginning of a round.
2. Players submit bids (can be fractional) in the range [0, maximum value].
3. The highest bidder(s) win the auction.
4. Payoffs are calculated based on the specific auction variation.
5. Players' capital is updated according to their payoffs.
6. Bots with no remaining capital are eliminated from future rounds.

## Auction Variations
1. **Variation 1**: Uniform distribution, payoff = x_i - bid
2. **Variation 2**: Uniform distribution, payoff = X - bid (X is max of all x_i)
3. **Variation 3**: Similar to Variation 2, with an additional penalty for the second-highest bidder

## How to Use
1. Clone the repository:
   ```
   git clone https://github.com/asurixyz/AuctionBot.git
   ```
2. Navigate to the project directory:
   ```
   cd AuctionBot
   ```
3. Implement your strategy by modifying the `Template.py` file in the `Strategies` folder.
4. Run the simulation:
   ```
   python Variant_1.py  # For Variation 1
   python Variant_2.py  # For Variation 2
   python Variant_3.py  # For Variation 3
   ```
5. The Starter Codes for the Auction Bot can be found [here][https://github.com/asurixyz/AuctionBot) ](https://drive.google.com/drive/folders/1db-SIWq5bNb1nGuyTUacfls1iA8iwDpH?usp=drive_link]

## Developing Your Bot
- Modify the `make_bid` function in your strategy file.
- Ensure your bot doesn't exceed time (1 second per round) or memory (100 MB) limits.
- You can use any available Python library, but mention them in your report.

## Submission
- Submit your bot codes (Python files) following the naming convention: `ROLLNO_1.py`, `ROLLNO_2.py`, `ROLLNO_3.py`.
- Include a brief report explaining your strategy.
- Submit via the provided Google Form.

## Evaluation
- Bots will be tested against sample bots and then compete in groups of 20.
- Multiple rounds will be conducted to minimize luck factors.
- Evaluation focuses on strategy adaptability and robustness across different scenarios.

## Resources
- [Introduction to Random Variables](https://www.investopedia.com/terms/r/random-variable.asp)
- [Python Programming Basics](https://www.w3schools.com/python/python_intro.asp)
- [NumPy Library Tutorial](https://www.w3schools.com/python/numpy/numpy_intro.asp)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Thanks to all participants for their creative strategies and engagement in the competition.
- Special thanks to the organizers and judges for making this event possible.
