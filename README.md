## Redis Challenge
___

The main goal was to implement a simplified version of some of the basic functionalities provided by Redis.

For those who are not familiar with Redis: Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker.

#### General Notes

---

The core container is a standard python dictionary. Both structural changes to the core dictionary (adding and removing keys) and updating a value associated with a key are synced using locks and thus assuring atomicity for all operations. 

Expiration of values is dealt via an Expiration Manager which is scheduled to trigger close to the expiration time of an entry.
  
The `ZSET` structure is implemented using slightly adapted `AVL Trees`.

Also, I took some time to play a bit with Python decorators to achieve a coding structure that I believe is quite intuitive when dealing with REST APIs in other languages. Check the file `routing_decotaror.py` for more info on this.

#### Supported Commands

---

The supported commands are:
* SET: associates a value to a given key. A time to live (TTL) can also be set.
* GET: fetches a value associate with a key;
* DEL: removes a key-value entry.
* DBSIZE: gets the current number of entries.
* INCR: it increments the value of an entry.
* ZADD: add a score and a value to a ordered set (ZSET) associated with a given key.
* ZCARD: gets the current number of values inside a set associated with a given key.
* ZRANK: gets the current position of a value inside a set associated with a given key.
* ZRANGE: get a range of values by a desired score range inside a set associated with a given key.

#### Starting the server

Run the file `main.py` on the main folder.

#### Command Syntax

The server expects a json sent by POST to the `/cmd` endpoint.

```
json = {
    cmd: <command> 
    <parameter 1>: <value parameter 1>,
    <parameter 2>: <value parameter 2>,
    etc... 
}
```

Following all the supported commands.

| Command | Parameter 1 | Parameter 2 | Parameter 3 |
|---------|-------------|-------------|-------------|
|set| key:\<string> | value:\<string>| ex:\<number> (Optional TTL)|
|get| key:\<string> | 
|del| key:\<string> |
|dbsize|
|incr| key:\<string> |
|zadd| key:\<string> | score:\<number>| member:\<string>|
|zcard| key:\<string> |
|zrank| key:\<string> | member:\<string>|
|zrange| key:\<string> | start:\<number> |stop:\<number>|

#### Future TO-DO

---
I would like to evaluate the performance of other ordered data structures for the `ZSet`.
 
