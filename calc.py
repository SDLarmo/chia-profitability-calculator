import argparse
import requests

BLOCKS_PER_DAY = 4608
HOURLY_POWER_CONSUMPTION_PER_TB = 0.001
NETSPACE_API = "https://api-mainnet.pool.space/api/pool"
PRICE_API = "https://xchscan.com/api/chia-price"
COLORS = {
    "red": '\033[91m',
    "green": '\033[92m',
    "yellow": '\033[93m',
    "end": '\033[0m',
}


def main():
    args = parce_cli_input()
    farm_power_consumption_per_hour = (
        args.farm_size * HOURLY_POWER_CONSUMPTION_PER_TB
        if args.power_consumption is None
        else args.power_consumption * 0.001
    )
    current_blockchain_size_tib = get_blockchain_size()
    hours_to_win = get_time_to_win(args.farm_size, current_blockchain_size_tib)
    chia_price = get_chia_price()
    power_price = get_power_price(hours_to_win, args.power_price, farm_power_consumption_per_hour)
    profit_per_day = get_profitability(chia_price, power_price, hours_to_win, 24)
    power_price_threshold = get_power_price_threshold(chia_price, hours_to_win, farm_power_consumption_per_hour)

    print(f"{COLORS['red'] if profit_per_day < 0 else COLORS['green']}"
          f"With {args.farm_size} TB you would {'lose' if profit_per_day < 0 else 'get'}:\n"
          f"  {round(abs(profit_per_day), 4)}$ per day\n"
          f"  {round(abs(profit_per_day) * 30, 4)}$ per month\n"
          f"  {round(abs(profit_per_day) * 365, 4)}$ per year\n"
          f"{COLORS['end']}"
          f"{COLORS['yellow']}Power price threshold is {round(power_price_threshold, 4)}$ per kW{COLORS['end']}")


def parce_cli_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--farm_size', type=float, help='Farm size in TB')
    parser.add_argument('-p', '--power_price', type=float, help='Power price in USD')
    parser.add_argument('-c', '--power_consumption', type=float, required=False, help='Power consumption in Watts')

    return parser.parse_args()


def get_blockchain_size():
    # gets current size of blockchain from the space pool API
    response = requests.get(NETSPACE_API)
    size_tib = response.json()["totalNetSpaceTiB"]

    return size_tib


def get_time_to_win(farm_size_tb, current_blockchain_size_tib):
    # calculates how many hours are required to win 1 block
    farm_size_tib = farm_size_tb * 0.909495
    prob_to_win_in_one_tick = farm_size_tib/current_blockchain_size_tib
    prob_to_win_in_one_day = 1 - (1 - prob_to_win_in_one_tick)**BLOCKS_PER_DAY

    return 1 / prob_to_win_in_one_day * 24


def get_chia_price():
    # gets current chia price in USD from the xchscan API
    response = requests.get(PRICE_API)
    price = response.json()["usd"]

    return price


def get_power_price(hours_to_win, electricity_price_per_kw, farm_power_consumption_per_hour):
    # calculates electricity cost required to win 1 block
    hourly_power_price = electricity_price_per_kw * farm_power_consumption_per_hour
    return hours_to_win * hourly_power_price


def get_profitability(chia_price, power_price, hours_to_win, mining_time_hours):
    # calculates profit per given amount of hours based on the current chia price and electricity price
    return (chia_price - power_price) / hours_to_win * mining_time_hours


def get_power_price_threshold(chia_price, hours_to_win, farm_power_consumption_per_hour):
    # calculates profitability threshold
    return chia_price / (hours_to_win * farm_power_consumption_per_hour)


if __name__ == "__main__":
    main()
