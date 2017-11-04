# Core project of the Crypto Fund.

## What is it for?

- Price arbitrage between markets
- Market making
- Time Series forecasting

## Installation

```
virtualenv -p python3 venv
source venv/bin/activate
git clone https://github.com/crypto-fund/core.git
cd core
pip3 install -r requirements.txt
python3 training.py # no need to have credentials to train.
```
## Simulation

```
cd simulator
export PYTHONPATH=../:$PYTHONPATH; python3 main.py
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

In another terminal tab, run:

```
cp credentials.json.example credentials.json # for simulation you don't need credentials but you need credentials.json.
curl -X POST http://127.0.0.1:5000/v2/balance/ # should display a nice JSON with all the variables.
# in constant.py, ADMIN_PROD_FLAG = False (by default)
python3 start_trading.py

# wait a few minutes
# Ctrl+C will quit the run script and finishes by a mass cancel of all open orders.

curl -X POST http://127.0.0.1:5000/v2/balance/

# expect the eur_available, eur_balance to be slightly different.
```
