# dummy-logger

## Don't use this!  

I am just messing around with end points for a JSON logging service, actual storage is garbage -- no effort towards throughput or guaranteed delivery of messages.

## Usage (but don't do it)

### Environment Variables

```ROOT_PATH``` - where to write the log.  Defaults to ```./logs```

```PORT``` - port to listen on, defaults to 5000

### Starting Server

```python server.py``` runs default flask

Or use starphleet to autodeploy.

### Writing a log message

Request:
```
curl -H "Content-Type: application/json" -X POST -d '{"channel": "demo", "data": {"username":"xyz","password":"xyz"}}' http://localhost:5000/
```

Response:
```
{"count": 1, "channel": "demo"}
```
```count``` is the number of messages in the log.  ```channel``` is the channel extracted from the message, defaults to ```"."```.


### Reading a log
Request:
```
curl 'http://localhost:5000/demo?limit=5'
```
Retrieves up to 5 messages from ```demo``` channel

Response:
```
[{"data": {"username": "xyz", "password": "xyz"}, "channel": "demo"}]
```
