python3 clean_price_data.py --data_dir /home/premy/projects/record-market/price_btc_usd/out --output_file ../data_examples/btc_price_$(date +"%m_%d_%Y-%H:%M:%S").csv
python3 clean_price_data.py --data_dir /home/premy/projects/record-market/price_eth_usd/out --output_file ../data_examples/eth_price_$(date +"%m_%d_%Y-%H:%M:%S").csv
python3 read_order_book.py --data_dir /home/premy/projects/record-market/ob_btc_usd/out --output_file ../data_examples/ob_btc_price_$(date +"%m_%d_%Y-%H:%M:%S").csv --order_book_desired_depth 20
python3 read_order_book.py --data_dir /home/premy/projects/record-market/ob_eth_usd/out --output_file ../data_examples/ob_eth_price_$(date +"%m_%d_%Y-%H:%M:%S").csv ----order_book_desired_depth 20
