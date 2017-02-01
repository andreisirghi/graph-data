## Create virtualenv
```
virtualenv -ppython3 venv
source venv/bin/activate
pip install -r requirements.txt # install dependencies
pip install -e . # install package itself
```

For available commands and config parameters run

```
graph-data --help
```

**Generate 200 students in a single batch to stdout** 

```
graph-data --batch_size 200 batch
```

**Generate 500 batches, each containing 200 students into `/tmp/dump` directory**
```
graph-data --batches 500 -- --batch_size 200 --output_dir /tmp/dump dump
```

