"""CSC 161 Project: Milestone III

Chirath Illukpitiya
Lab Section TR 12:30- 1:45pm
Fall 2021
"""


def categories(filedata):
    one, two, three, four, five, six, seven = [], [], [], [], [], [], []
    setdata = [one, two, three, four, five, six, seven]
    for line in filedata:
        Date, Open, High, Low, Close, Adj_close, Volume = line.split(",")
        one.append(Date)
        two.append(Open)
        three.append(High)
        four.append(Low)
        five.append(Close)
        six.append(Adj_close)
        seven.append(Volume)
    return setdata


def get_data(data, col, day):
    if col == "date":
        price = (data[0])[day]
    if col == "open":
        price = (data[1])[day]
        price = float(price)
    if col == "high":
        price = (data[2])[day]
        price = float(price)
    if col == "low":
        price = (data[3])[day]
        price = float(price)
    if col == "close":
        price = (data[4])[day]
        price = float(price)
    if col == "adj_close":
        price = (data[5])[day]
        price = float(price)
    if col == "volume":
        price = (data[6])[day]
        price = int(price)
    return price


def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

    Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    file = open(filename, 'r')
    data = file.readlines()
    file.close()
    data = categories(data)
    price = get_data(data, col, day)
    return price


def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float; it is a value of how much money you have,
                  currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters
           are both set to true, or both false. You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.
    """
    if buy is True and sell is True:
        raise ValueError("Ambigious transaction!"
                         "Can't determine whether to buy or sell.")
        return funds, stocks
    if buy is False and sell is False:
        raise ValueError("Ambigious transaction!"
                         "Can't determine whether to buy or sell.")
        return funds, stocks
    if sell is True:
        if buy != sell and stocks >= qty:
            cash_balance = funds + (qty * price)
            stocks_owned = stocks - qty
            return float(cash_balance), int(stocks_owned)
        else:
            raise ValueError("Insufficient stocks owned to sell {0} stocks!"
                             .format(qty))
            return funds, stocks
    if buy is True:
        if buy != sell and funds >= qty * price:
            cash_balance = funds - (qty * price)
            stocks_owned = stocks + qty
            return float(cash_balance), int(stocks_owned)
        else:
            raise ValueError("Insufficient funds to purchase {0} at ${1:0.2f}! "
                             .format(qty, price))
            return funds, stocks


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower
      than the moving average.
    - You must sell shares if the current day price is 5%, or more, higher,
      than the moving average.
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Args:
        A filename, as a string.

    Returns:
        Note: You *must* sell all your stock before returning.
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """
    low = []
    file = open(filename, "r")
    file.readline()
    for line in file:
        l0w = line.split(",")
        low.append(float(l0w[3]))
    cash_balance, stocks_owned, stock, all_, moving_avg = 1000, 0, 10, [0], []
    day = 20
    for i, all_days in enumerate(low, 1):
        all_.append(all_[i - 1] + all_days)
        if i >= day:
            avg = (all_[i] - (all_[i - day]))/day
            moving_avg.append(float(avg))
    for i in range(len(moving_avg) - 1):
        if stocks_owned >= stock:
            if low[day + i] >= (moving_avg[i] + (moving_avg[i]/(1/.05))):
                cash_balance, stocks_owned = transact(cash_balance,
                                                      stocks_owned, stock,
                                                      low[20 + i],
                                                      buy=False, sell=True)
        elif cash_balance >= (stock * low[i + day]):
            if low[day + i] <= (moving_avg[i] - (moving_avg[i]/(1/.05))):
                cash_balance, stocks_owned = transact(cash_balance,
                                                      stocks_owned, stock,
                                                      low[20 + i],
                                                      buy=True, sell=False)
        else:
            continue
    cash_balance = cash_balance + (stocks_owned * low[-1])
    stocks_owned = 0

    # Last thing to do, return two values: one for the number of stocks you end
    # up owning after the simulation, and the amount of money you have after
    # the simulation.  Remember, all your stocks should be sold at the end!
    return stocks_owned, cash_balance


def alg_rsi(filename_1, filename_2):
    """This function implements the Relative Strength Index algorithm.

    Using the CSV stock data from two stock files that are loaded into your
    program, use that data to make decisions using the Relative Strength
    Index (RSI) algorithm.

    Algorithm:
        [REPLACE THIS WITH A CLEAR DESCRIPTION OF THE ALGORITHM.]
        [I AM LEAVING THIS YOUR RESPONSIBILITY TO FILL OUT.]

    Arguments:
        filename_1 (str): A filename, as a string, for one set of stock
                          data for a first company.

        filename_2 (str): A filename, as a string, for one set of stock
                          data for a second company.

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """

    # Last thing to do, return two values: one for the number of stocks you
    # end up owning after the simulation, and the amount of money you have
    # after the simulation. Remember, all your stocks should be sold at the
    # end!
    cash_balance = 10000
    low_apple = []
    low_micro = []
    file = open(filename_1, "r")
    file.readline()
    for line in file:
        l0w = line.split(",")
        low_apple.append(float(l0w[3]))
    file.close
    file_2 = open(filename_2, "r")
    file_2.readline()
    for line in file_2:
        l0W = line.split(",")
        low_micro.append(float(l0W[3]))
    file_2.close
    gain_apple = []
    loss_apple = []
    gain_micro = []
    loss_micro = [] 
    i = 0
    j = 0
    while i < len(low_apple):
        if i == 0:
            gain_apple.append(0)
            loss_apple.append(0)
        if low_apple[i] - low_apple[i - 1] > 0 and i != 0:
            gain_apple.append(low_apple[i] - low_apple[i - 1])
            loss_apple.append(0)
        if low_apple[i] - low_apple[i - 1] < 0 and i != 0:
            gain_apple.append(0)
            loss_apple.append(low_apple[i] - low_apple[i - 1] < 0)
        i += 1
    while j < len(low_micro):
        if j == 0:
            gain_micro.append(0)
            loss_micro.append(0)
        if low_micro[j] - low_micro[j - 1] > 0 and j != 0:
            gain_micro.append(low_micro[j] - low_micro[j - 1])
            loss_micro.append(0)
        if low_micro[j] - low_micro[j - 1] < 0 and j != 0:
            gain_micro.append(0)
            loss_micro.append(low_micro[j] - low_micro[j - 1] < 0)
        j += 1
    day = 0
    day2 = 0
    sum_micro_gain = 0
    sum_micro_loss = 0
    x2 = day2 - 21
    avg_apple_gain = []
    avg_apple_loss = []
    avg_micro_gain = []
    avg_micro_loss = []
    while day < len(gain_apple):
        if day < 22:
            avg_apple_gain.append(0)
            avg_apple_loss.append(0)
        else:
            sum_apple_gain = 0
            sum_apple_loss = 0
            x = day - 21
            while x <= day:
                sum_apple_gain += gain_apple[x]
                sum_apple_loss += loss_apple[x]
                x += 1
            avg_apple_gain.append(sum_apple_gain/21)
            avg_apple_loss.append(abs(sum_apple_loss/21))
        day += 1
    while day2 < len(gain_micro):
        if day2 < 22:
            avg_micro_gain.append(0)
            avg_micro_loss.append(0)
        else:
            sum_micro_gain = 0
            sum_micro_loss = 0
            x2 = day2 - 21
            while x2 <= day2:
                sum_micro_gain += gain_micro[x2]
                sum_micro_loss += loss_micro[x2]
                x2 += 1
            avg_micro_gain.append(sum_micro_gain/21)
            avg_micro_loss.append(abs(sum_micro_loss/21))
        day2 += 1
    rsi_day = 0
    rsi_day2 = 0
    rsi_apple = []
    rsi_micro = []
    while rsi_day < len(gain_apple):
        if rsi_day < 22:
            rsi_apple.append(0)
        else:
            simplifier = avg_apple_gain[rsi_day]/avg_apple_loss[rsi_day]
            rsi_apple.append(100 - (100 / (1 + simplifier)))
        rsi_day += 1
    while rsi_day2 < len(gain_micro):
        if rsi_day2 < 22:
            rsi_micro.append(0)
        else:
            simplify = avg_micro_gain[rsi_day2]/avg_micro_loss[rsi_day2]
            rsi_micro.append(100 - (100 / (1 + simplify)))
        rsi_day2 += 1
    stocks_owned_a = 0
    cash_balance_a = 10000
    cash_balance_m = 10000
    stocks_owned_m = 0
    for i in range(len(rsi_apple)):
        if stocks_owned_a >= 5 and rsi_apple[i] < 30:
            cash_balance_a, stocks_owned_a = transact(cash_balance_a,
                                                      stocks_owned_a,
                                                      5, low_apple[i],
                                                      False, True)
        elif cash_balance_a >= (5 * low_apple[i]) and rsi_apple[i] > 70:
            cash_balance_a, stocks_owned_a = transact(cash_balance_a,
                                                      stocks_owned_a,
                                                      5, low_apple[i],
                                                      True, False)
        else:
            continue
        
    for i in range(len(rsi_micro)):
        if stocks_owned_m >= 5 and rsi_micro[i] < 30:
            cash_balance_m, stocks_owned_m = transact(cash_balance_m,
                                                      stocks_owned_m,
                                                      5, low_micro[i],
                                                      False, True)
        elif cash_balance_m >= (5 * low_micro[i]) and rsi_micro[i] > 70:
            cash_balance_m, stocks_owned_m = transact(cash_balance_m,
                                                      stocks_owned_m,
                                                      5, low_micro[i],
                                                      True, False)
        else:
            continue
    cash_balance_a += (stocks_owned_a * low_apple[-1])
    cash_balance_m += (stocks_owned_m * low_micro[-1])
    stocks_owned_a = 0
    stocks_owned_m = 0
    cash_balance = cash_balance_a + cash_balance_m
    stocks_owned = stocks_owned_a + stocks_owned_m
            
    return stocks_owned, cash_balance

    
# Don't forget the required "__main__" check!
def main():
    # My testing will use AAPL.csv or MSFT.csv
    stock_file_1 = input("Enter a filename for stock data (in CSV format): ")

    # Call your moving average algorithm, with the filename to open.
    alg1_stocks, alg1_balance = alg_moving_average(stock_file_1)

    # Print results of the moving average algorithm, returned above:
    print("The results are...")

    # Now, call your RSI algorithm!
    stock_file_2 = input("Enter another filename for second stock data"
                         "file (in CSV format): ")
    alg2_stocks, alg2_balance = alg_rsi(stock_file_1, stock_file_2)

    # Print results of your algorithm, returned above:
    print("The results are...")
    print(alg2_stocks, alg2_balance)


if __name__ == '__main__':
    main()
