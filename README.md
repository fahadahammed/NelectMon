# NelectMon
Network + Electricity Monitoring tool with MongoDB, gRPC, Python, Python Flask.

## How To?

### Webapp
#### Python
```shell
python3 run.py
```
#### uwsgi
```shell
uwsgi --
```

### Worker
```shell
rq worker -c src.library.theworker
```