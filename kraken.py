import websocket
import json

class KrakenClient():
    """
    Opens a websocket to Kraken and pulls best current bid/ask for BTC/USD
    """

    def __init__(self):
        """
        initialize variables
        """
        self.ws = None

    def on_message(self, ws, message):
        """
        Prints best bid/ask and size
        """
        message = json.loads(message)
        data = message[1]
        print(f"Kraken: best bid: {data['b'][0]}, bid size: {data['b'][2]}, best ask: {data['a'][0]}, ask size: {data['a'][2]}")

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
        Subscribes to the ticker channel
        """
        params = json.dumps({'event': 'subscribe', 'subscription': {'name':'ticker'}, 'pair': ['BTC/USD']})
        print(f'Connected to Kraken...\n')
        ws.send(params)

    def connect(self):
        """
        Creates and starts websocket
        """
        self.ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
        self.ws.run_forever()

if __name__ == "__main__":
    k = KrakenClient()
    k.connect()
