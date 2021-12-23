import websocket
import json

class FtxClient():
    """
    Opens a websocket to FTX US and pulls best current bid/ask for BTC/USD
    """

    def __init__(self):
        """
        Initialize variables
        """
        self.ws = None

    def on_message(self, ws, message):
        """
        Prints best bid/ask and size
        """
        message = json.loads(message)
        data = message['data']
        print(f"FTX US: best bid: {data['bid']}, bid size: {data['bidSize']}, best ask: {data['ask']}, ask size: {data['askSize']}")

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
        params = json.dumps({'op': 'subscribe', 'channel': 'ticker', 'market': 'BTC/USD'})
        print(f'Connected to FTX US\n')
        ws.send(params)

    def connect(self):
        """
        Creates and starts websocket
        """
        self.ws = websocket.WebSocketApp("wss://ftx.us/ws/", on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
        self.ws.run_forever()  
    

if __name__ == "__main__":
    f = FtxClient()
    f.connect()

