import requests
import json

# while true;
# do wget https://www.bitstamp.net/api/order_book -O out/$(date -d "today" +"%Y%m%d-%H%M%S").json;
# sleep 5; done;

if __name__ == '__main__':
    end_point = 'https://www.bitstamp.net/api/order_book'
    r = requests.get(end_point)
    r_json = json.loads(r.content.decode('utf8'))
    r_json['bids'] = r_json['bids'][0:20]
    r_json['asks'] = r_json['asks'][0:20]
    with open('out/' + r_json['timestamp'] + '.json', 'w') as f:
        json.dump(r_json, indent=4, fp=f)
