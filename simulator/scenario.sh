#!/usr/bin/env bash
curl -X POST http://127.0.0.1:5000/balance/
echo ""
echo ""

curl -X POST http://127.0.0.1:5000/buy/market/btceur/ -d "amount=0.03"

curl -X POST http://127.0.0.1:5000/balance/
echo ""
echo ""

curl -X POST http://127.0.0.1:5000/sell/market/btceur/ -d "amount=0.03"

curl -X POST http://127.0.0.1:5000/balance/
echo ""
echo ""
