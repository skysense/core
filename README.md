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
```

## Start to trade on the simulator

### Run the simulator

```
cd simulator
export PYTHONPATH=../:$PYTHONPATH; python3 main.py
# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Run the trader

In another terminal tab, run:

```
cp credentials.json.example credentials.json # for simulation you don't need valid credentials but you need credentials.json.
curl -X POST http://127.0.0.1:5000/v2/balance/ # should display a nice JSON with all the variables.
# in constant.py, ADMIN_PROD_FLAG = False (by default)
python3 start_trading.py

# wait a few minutes
# Ctrl+C will quit the run script and will finish by a mass cancel of all open orders.

curl -X POST http://127.0.0.1:5000/v2/balance/

# expect the eur_available, eur_balance to be slightly different.
```

The model deployed here is a dummy model whose weights are in `MODEL_CHECKPOINTS_DIR = dummy_checkpoints`.

The next section is about training.

## Training

In this section, we're going to see how:

- to train a model from scratch
- the correct format and conventions to make a nice interoperability with the inference part.

Start a training is actually very simple. Here's how to start it for the dummy model (model_0):

```
rm -rf dummy_checkpoints/*
python3 model_training/model_0_training.py
ls -l dummy_checkpoints # should contain some files!
```

Those weights are in the right format for inference.

The inference task expects two main things:

- a specific naming to retrieve the nodes easily:

```
MODEL_INPUT_TENSOR_NAME = 'Input/ClosePrices'
MODEL_OUTPUT_TENSOR_NAME = 'Output/Prediction'
```

- 3 outputs for the output node (should be `buy`, `hold` and `sell` confidence and they should add up to 1).

A simple model graph filling all those requirements are:

```
import tensorflow as tf
import tensorflow.contrib.slim as slim
from easy_model_saving import model_saver

input_close_prices = tf.placeholder(tf.float32, shape=[None, 1], name=MODEL_INPUT_TENSOR_NAME)
m = slim.fully_connected(inputs=input_close_prices, num_outputs=20, activation_fn=tf.nn.relu)
softmax_output = slim.fully_connected(inputs=m, num_outputs=3, activation_fn=tf.nn.softmax)
tf.identity(softmax_output, name=MODEL_OUTPUT_TENSOR_NAME)
```

`[None, 1]` will be updated to `[None, sequence_length]` where `sequence_length` is the lookback window of the LSTM model.

A simple training procedure looks like this:

```
import tensorflow as tf
import tensorflow.contrib.slim as slim
from easy_model_saving import model_saver

def run_dummy_training():
    with tf.Session() as sess:
        graph()
        sess.run(tf.global_variables_initializer())
        saver = model_saver.Saver(MODEL_CHECKPOINTS_DIR)
        saver.save(global_step=10)

        last_step = model_saver.restore_graph_variables(MODEL_CHECKPOINTS_DIR)
        assert last_step != 0
```

All those snippets are from `model_training/model_0_training.py`.

That's it!
