

from kafka import KafkaProducer
import websocket
import json
import os
from dotenv import load_dotenv

load_dotenv() 


key = os.getenv('FINNHUB_API_KEY')
kafka_servers = os.getenv('KAFKA_SERVERS').split(',')  # 'Kafka00Service:9092'

kafka_producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda msg: json.dumps(msg).encode('utf-8'),
)

def on_message(ws, message):
    try:
        msg = json.loads(message)
        for price in msg["data"]:
            data = {
                'symbol': str(price['s']),
                'last_price': str(price['p']),
                'timestamp': str(price['t']),
                'volume': str(price['v']),
                'trade_conditions': str(price['c']),
            }
            print(data)
            kafka_producer.send(
                topic='price',
                value=data,
                key=json.dumps(price['s']).encode('utf-8')
            )
    except Exception as e:
        print('ERROR => ', e)
        raise
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"META"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"NFLX"}')
    ws.send('{"type":"subscribe","symbol":"GOOGL"}')
    ws.send('{"type":"subscribe","symbol":"AAPL"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={key}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    
    ws.on_open = on_open
    ws.run_forever()