import websocket
import json
from copy import deepcopy

class CoinbaseClient():
    """
    Opens a websocket to Coinbase API, constructs an order book, and pulls best current bid/ask for BTC/USD
    """

    def __init__(self):
        """
        initialize variables
        """
        self.ws = None
        self.order_book = None

    def on_message(self, ws, message):
        """
        Sets the orderbook and calls process_orderbook for updates
        """
        message = json.loads(message)

        # inital order book
        if message['type'] == 'snapshot':
            self.order_book = deepcopy(message)
            # convert bids and asks from str to float
            for i, pair in enumerate(self.order_book['asks']):
                self.order_book['asks'][i][0], self.order_book['asks'][i][1] = float(pair[0]), float(pair[1])
            for i, pair in enumerate(self.order_book['bids']):
                self.order_book['bids'][i][0], self.order_book['bids'][i][1] = float(pair[0]), float(pair[1])
        elif message['type'] == 'l2update':
            # cast price and size as float
            self.process_orderbook(message['changes'][0][0], float(message['changes'][0][1]), float(message['changes'][0][2]))
        # print bids and asks at top of book
        print(f"Coinbase: best bid: {self.order_book['bids'][0][0]}, bid size: {self.order_book['bids'][0][1]}, best ask: {self.order_book['asks'][0][0]}, ask size: {self.order_book['asks'][0][1]}")

    def process_orderbook(self, side, price, size):
        """
        Takes l2update params and makes necessary adjustments to orderbook
        """
        # if the buy side update is of size 0 then the level can be cleared (from bids) otherwise update or enter
        # the new value into the ordered location
        # if the sell side update is of size 0 then the new level can be cleared from (asks) otherwise update or
        # enter the new value into the ordered location
        if side == 'buy':
            for i, pair in enumerate(self.order_book['bids']):
                if price == pair[0]:
                    if size == 0:
                        del self.order_book['bids'][i]
                    else:
                        self.order_book['bids'][i][1] = size
                    return
                elif price > pair[0]:
                    self.order_book['bids'].insert(i, [price, size])
                    return
                # at the end so we can append
                elif i == len(self.order_book['bids']) - 1:
                    self.order_book['bids'].append([price, size])
        elif side == 'sell':
            for i, pair in enumerate(self.order_book['asks']):
                if price == pair[0]:
                    if size == 0:
                        del self.order_book['asks'][i]
                    else:
                        self.order_book['asks'][i][1] = size
                    return
                elif price < pair[0]:
                    self.order_book['asks'].insert(i, [price, size])
                    return
                elif i == len(self.order_book['asks']) - 1:
                    self.order_book['asks'].append([price, size])
                    return

    def on_error(self, ws, error):
        """
        """
        print(error)

    def on_close(self, ws):
        """
        """
        print("### closed ###")

    def on_open(self, ws):
        """
        Subscribes to the level2 channel
        """
        params = json.dumps(
            {
                "type": "subscribe",
                "product_ids": [
                    "BTC-USD"
                ],
                "channels": ["level2"]
            }
            )
        print(f'Connected to Coinbase...\n')
        ws.send(params)

    def connect(self):
        """
        Creates and starts websocket
        """
        self.ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com", on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
        self.ws.run_forever()


if __name__ == "__main__":
    c = CoinbaseClient()
    c.connect()