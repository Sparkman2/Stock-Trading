"""Stock Trading Algorithim"""

def categories(filedata):
    set_data = [[] for _ in range(7)]
    for line in filedata:
        values = line.strip().split(',')
        for i in range(7):
            set_data[i].append(values[i])
    return set_data


def get_data(data, col, day):
    col_idx = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'adj_close': 5, 'volume': 6}[col]
    price = data[col_idx][day]
    if col in {'open', 'high', 'low', 'close', 'adj_close'}:
        price = float(price)
    elif col == 'volume':
        price = int(price)
    return price


def test_data(filename, col, day):

    """A test function to query the data you loaded into your program."""

    with open(filename, 'r') as file:
        data = file.readlines()
    data = categories(data)
    price = get_data(data, col, day)
    return price


def transact(funds, stocks, qty, price, buy=False, sell=False):

    """A bookkeeping function to help make stock transactions.

        funds (float): Available funds for the transaction
        stocks (int): Number of stocks owned
        qty (int): Number of stocks to buy or sell
        price (float): Price of each stock
        buy (bool, optional): Whether to buy stocks (default is False)
        sell (bool, optional): Whether to sell stocks (default is False)

    """

    # Check if the transaction is ambiguous
    if buy == sell:
        raise ValueError("Ambiguous transaction! Can't determine whether to buy or sell.")

    # Sell stocks
    if sell:

        # Check if there are enough stocks to sell
        if stocks < qty:
            raise ValueError("Insufficient stocks owned to sell {0} stocks!".format(qty))
        funds += qty * price
        stocks -= qty

    # Buy stocks
    else:

        # Check if there are enough funds to buy the stocks
        if funds < qty * price:
            raise ValueError("Insufficient funds to purchase {0} at ${1:0.2f}!".format(qty, price))
        funds -= qty * price
        stocks += qty

    return funds, stocks


def alg_moving_average(filename, day):
    """This function implements the moving average stock trading algorithm"""

    low = []
    file = open(filename, "r")
    file.readline()
    for line in file:
        l0w = line.split(",")
        low.append(float(l0w[3]))
    cash_balance, stocks_owned, stock, moving_avg = 1000, 0, 10, []

    # Calculate moving average for each day
    for i in range(day - 1, len(low)):
        avg = sum(low[i - day + 1:i + 1]) / day
        moving_avg.append(avg)

    # Buy or sell stocks based on moving average
    for i in range(len(moving_avg) - 1):
        if stocks_owned >= stock:
            # If stocks_owned is greater than or equal to the desired number of stocks, try to sell
            if low[day + i] >= (moving_avg[i] + (moving_avg[i] / (1 / .05))):
                cash_balance, stocks_owned = transact(cash_balance, stocks_owned, stock, low[day + i], buy=False,
                                                      sell=True)
        elif cash_balance >= (stock * low[i + day]):
            # If cash_balance is greater than or equal to the cost of buying the desired number of stocks, try to buy
            if low[day + i] <= (moving_avg[i] - (moving_avg[i] / (1 / .05))):
                cash_balance, stocks_owned = transact(cash_balance, stocks_owned, stock, low[day + i], buy=True,
                                                      sell=False)
        else:
            # If neither of the above conditions are met, do nothing
            continue

    # Calculate the final cash balance after selling all remaining stocks
    cash_balance = cash_balance + (stocks_owned * low[-1])
    stocks_owned = 0
    return stocks_owned, cash_balance


def alg_rsi(filename):

    """This function implements the RSI stock trading algorithm"""

    file = open(filename, "r")
    file.readline()
    price_data = []

    # Loop through the lines in the file and append the closing prices to the list
    for line in file:
        values = line.split(",")
        price_data.append(float(values[4]))  # closing price

    funds, stocks_owned, stock = 1000, 0, 10

    # Loop through the price data
    for i in range(14, len(price_data)):
        avg_gain = 0
        avg_loss = 0

        # Calculate the average gain and average loss for the past 14 days
        for j in range(i - 14, i):
            diff = price_data[j + 1] - price_data[j]
            if diff > 0:
                avg_gain += diff
            else:
                avg_loss += abs(diff)
        avg_gain /= 14
        avg_loss /= 14

        # Calculate the RSI based on the average gain and average loss
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        # Buy or sell stocks using transact function based on the RSI and current funds and stock ownership
        if stocks_owned >= stock:
            if rsi >= 70:
                funds, stocks_owned = transact(funds, stocks_owned, stock, price_data[i], buy=False, sell=True)
        elif funds >= stock * price_data[i]:
            if rsi <= 30:
                funds, stocks_owned = transact(funds, stocks_owned, stock, price_data[i], buy=True, sell=False)
        else:
            continue

    # Calculate the final cash balance after all transactions
    cash_balance = funds + (stocks_owned * price_data[-1])
    stocks_owned = 0

    return stocks_owned, cash_balance



def main():

    # Prompt user for input files and algorithm parameters
    stock_file = input("Enter a filename for stock data (in CSV format): ")
    days = int(input("Enter the number of days for the moving average algorithm: "))

    # Call your moving average algorithm, passing in the filename and number of days
    alg1_stocks, alg1_balance = alg_moving_average(stock_file, days)

    print("The results are...")
    print(alg1_stocks, alg1_balance)

    stock_file2 = input("Enter a filename for stock data (in CSV format): ")

    # Call your rsi algorithm, passing in the filename
    alg2_stocks, alg2_balance = alg_rsi(stock_file2)

    print("The results are...")
    print(alg2_stocks, alg2_balance)

if __name__ == '__main__':
    main()
