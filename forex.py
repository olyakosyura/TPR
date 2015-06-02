import random
import math

MAX_FORECAST = 6.0
FORECAST_MIN_PRECISION = 90.0

class Broker(object):
    def beliver_statagy(self, market):
        if (market.rubles_sold == market.rubles_bought == 0.0):
            print ('%s skip turn' % self.name)
            return
        if market.rubles_sold > market.rubles_bought:
            market.sell(self.rubles, self.name)
            new_dollars = self.rubles / market.exchange_rate
            self.rubles = 0.0
            self.dollars += new_dollars
        else:
            new_rubles = self.dollars * market.exchange_rate
            market.buy(new_rubles, self.name)
            self.dollars = 0.0
            self.rubles += new_rubles

    def market_analizer_stratagy(self, market):
        percent_to_do = math.fabs(market.get_forecast()) / MAX_FORECAST * 100 
        print ("percent_to_do = %s" % percent_to_do)
        if market.get_forecast() > 0.0:
            rubles_to_sell = self.rubles / 100.0 * percent_to_do
            new_dollars = rubles_to_sell / market.exchange_rate
            self.rubles -= rubles_to_sell
            self.dollars += new_dollars
            market.sell(rubles_to_sell, self.name)
        elif market.get_forecast() < 0.0:
            dollars_to_sell = self.dollars / 100.0 * percent_to_do
            new_rubles = dollars_to_sell * market.exchange_rate
            self.dollars -= dollars_to_sell
            self.rubles += new_rubles
            market.buy(new_rubles, self.name)

    def random_stratagy(self, market):
        percent_to_do = 100.0 
        if random.random() < 0.5:
            rubles_to_sell = self.rubles / 100.0 * percent_to_do
            new_dollars = rubles_to_sell / market.exchange_rate
            self.rubles -= rubles_to_sell
            self.dollars += new_dollars
            market.sell(rubles_to_sell, self.name)
        elif random.random() < 0.5 > 0.0:
            dollars_to_sell = self.dollars / 100.0 * percent_to_do
            new_rubles = dollars_to_sell * market.exchange_rate
            self.dollars -= dollars_to_sell
            self.rubles += new_rubles
            market.buy(new_rubles, self.name)
        
    def all_in_stratagy(self, market):
        percent_to_do = 100.0 
        if market.get_forecast() > 0.0:
            rubles_to_sell = self.rubles / 100.0 * percent_to_do
            new_dollars = rubles_to_sell / market.exchange_rate
            self.rubles -= rubles_to_sell
            self.dollars += new_dollars
            market.sell(rubles_to_sell, self.name)
        elif market.get_forecast() < 0.0:
            dollars_to_sell = self.dollars / 100.0 * percent_to_do
            new_rubles = dollars_to_sell * market.exchange_rate
            self.dollars -= dollars_to_sell
            self.rubles += new_rubles
            market.buy(new_rubles, self.name)


    def __init__(self, name, dollars, rubles, stratagy):
        self.dollars = dollars
        self.rubles = rubles
        self.name = name
        self.stratagy = None
        if stratagy == 'beliver_statagy':
            self.stratagy = self.beliver_statagy
        elif stratagy == 'analizer_stratagy':
            self.stratagy = self.market_analizer_stratagy
        elif stratagy == 'allin':
            self.stratagy = self.all_in_stratagy
        elif stratagy == 'random':
            self.stratagy = self.random_stratagy

    def turn(self, market):
        self.stratagy(market)


class Market(object):
    def __init__(self, brokers):
        self.brokers = brokers
        self.exchange_rate = 50.0 + (1 - 2 * random.random())
        print("Staring exchange rate is %s" % self.exchange_rate)
        self.forecast = MAX_FORECAST - 2 * MAX_FORECAST * random.random() #IN PERCENTS
        self.rubles_sold = 0
        self.rubles_bought = 0

    def sell(self, sum, name):
        print('%s sells %d rubles' % (name, sum))
        #self.rubles_sold += sum
        self.rubles_sold += 1

    def buy(self, sum, name):
        print('%s buys %d rubles' % (name, sum))
        self.rubles_bought += 1
        #self.rubles_bought += sum

    def get_forecast(self):
        return self.forecast

    def turn(self):
        print ('New turn. Exchange rate %s. Forecast %s%%' % (self.exchange_rate, self.forecast))
        random.shuffle(self.brokers)
        self.rubles_sold = 0
        self.rubles_bought = 0
        for broker in self.brokers:
            broker.turn(self)
        incr = self.forecast / 100 * random.randint(FORECAST_MIN_PRECISION, 100)
        if math.fabs(incr) <= 3.6:
            incr = incr * random.choice([-1, -1, -1, -1, 1])
        self.exchange_rate = self.exchange_rate + self.exchange_rate / 100.0 * incr
        self.forecast = MAX_FORECAST - 2 * MAX_FORECAST * random.random()
        self.brokers.sort(key = lambda x: x.rubles + self.exchange_rate * x.dollars, reverse=True)
        for broker in self.brokers:
            print ("STAT FOR %s. Rubles = %s, dollars = %s, score = %s" % (broker.name, int(broker.rubles), int(broker.dollars), broker.rubles + self.exchange_rate * broker.dollars))

brokers = []
for i in range(0, 4):
    brokers.append(Broker("Beleiver_%s" % (i + 1), 1000.0, 50000.0, 'beliver_statagy'))
for i in range(0, 2):
    brokers.append(Broker("analizer_%s" % (i + 1), 1000.0, 50000.0, 'analizer_stratagy'))
for i in range(0, 3):
    brokers.append(Broker("allin_%s" % (i + 1), 1000.0, 50000.0, 'allin'))
for i in range(0, 12):
    brokers.append(Broker("random_%s" % (i + 1), 1000.0, 50000.0, 'random'))
market = Market(brokers)
for _ in range(0, 100):
    market.turn()
