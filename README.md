## Create virtualenv
```
virtualenv -ppython3 venv
source venv/bin/activate
pip install -r requirements.txt # install dependencies
pip install -e . # install package itself
```

For available commands and config parameters run

```
fake-students --help
```

##### Generate multiple students batches into given directory
```
fake-students --output_dir /tmp/gd/fakes/ dump
```

##### Generate single students batch

```
fake-students batch
```
