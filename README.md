# CHIA MINING PROFITABILITY CALCULATOR

### Run program:
1. Install Python 3;
2. Install requirements with `pip install -r requirements.txt`
3. Run program with: `python3 calc.py -f 300 -p 0.05 -c 200`

* -f, --farm_size - size of cryptocurrency farm in TB
* -p, --power_price - price of electricity per kW
* -c, --power_consumption - farm power consumption in W per hour (optional). If not provided a general consumption of 1W/TB will be used in the calculations.

### Description:
This project is made to calculate the profitability of mining Chia (XCH) coin. \
To get the profitability calculations user must provide farm size in TB, price per kW of power and total hourly power consumption (optional).
Chance to win a block depends on the network size and user's farm size. Network size is received via the API request and farm size must be provided by the user.
There are 4608 block mined per day and the reward is 1 chia coin per block.
So the formula for a daily win chance is:
```
daily_win_chance = 1 - (1 - farm_size / network_size)^4608
```
To calculate how profitable it is to mine Chia coin we should calculate the cost of electricity to mine 1 block.
The formula for calculating the electricity cost is next:
```
total_amount_of_hours_to_mine_one_block = 1 / daily_win_chance * 24
total_power_cost = total_amount_of_hours_to_mine_one_block * power_price_per_hour
```
To calculate profitability we just need to deduct electricity price, paid to mine one block, from the coin price.
Coin price is received via the API request.
To calculate the hourly profit we would need to divide one block profitability by number of hours that were used to mine that block.
```
profit_per_one_block = chia_cost - total_power_cost
hourly_profit = profit_per_one_block / hours_to_mine_one_block
```
Then we could easily use hourly_profit to calculate the profit for 1 day, 1 month and so on:
```
monthly_profit = hourly_profit * 24 * 30
```
To calculate the threshold price of electricity where mining becomes unprofitable we should divide chia price by the amount of hours to win 1 block and the farm power consumption per one hour.
```
power_price_threshold = chia_price / (hours_to_win * farm_power_consumption_per_hour)
```
