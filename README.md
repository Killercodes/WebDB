WebDB
===
A web based database


## Usage:

### List All Tables:
```bash
curl "http://localhost:5555/"
```

### Save Key-Value Pair:
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"name\", \"value\":\"thisdata\"}" "http://localhost:5555/web1"
curl -X POST "http://localhost:5555/web1?key=name&value=dave"
```
#### Here:
- `POST` - used to set new keyvalue into db
- `web1` - table name
- `key` - key value (string)
- `value` - data (string)

### Update Key-Value Pair:
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key":"name", "value":"updated value"}' "http://localhost:5555/web1"
curl -X PUT "http://localhost:5555/web1?key=name&value=john"
```
#### Here:
- `PUT` - used to update value into db
- `web1` - table name
- `key` - key value (string)
- `value` - data (string)

### Retrieve a Specific Key-Value Pair:
```bash
curl "http://localhost:5555/web1/name"
Here:
  GET - used to get new keyvalue into db
  web1 - table name
  name - key value (string)
```			
	
### List All Key-Value Pairs:
```bash
		curl "http://localhost:5555/web1"
```

###	Delete Key-Value Pair:
```bash
curl -X DELETE "http://localhost:5555/web1?key=name"
Here:
  DELETE - used to delete keyvalue from db
  web1 - table name
  key - key value (string)
```
	

