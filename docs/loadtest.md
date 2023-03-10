# Loadtesting create task api
Final results shows us that our web-server can handle 35 request per second.

```json
{
  "name": "task1",
  "creator": "1",
  "state": "2",
  "description": "description1",
  "members": "1"
}
```

```bash
ab -p docs/post_data.json -T application/x-www-form-urlencoded  -H 'Cookie: csrftoken=1ZmAh5v8pnV8Ov6mxG1ydQUCsge2o8eT; sessionid=o0opqd35vwf49rcteommwim9tiosu1kw' -c 1 -n 1000 http://localhost:8000/create-task/
```

# Results:
```text
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        WSGIServer/0.2
Server Hostname:        localhost
Server Port:            8000

Document Path:          /create-task/
Document Length:        0 bytes

Concurrency Level:      1
Time taken for tests:   28.110 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      317000 bytes
Total body sent:        419000
HTML transferred:       0 bytes
Requests per second:    35.57 [#/sec] (mean)
Time per request:       28.110 [ms] (mean)
Time per request:       28.110 [ms] (mean, across all concurrent requests)
Transfer rate:          11.01 [Kbytes/sec] received
                        14.56 kb/s sent
                        25.57 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       1
Processing:    14   28  11.3     26     156
Waiting:       13   27  11.1     25     155
Total:         14   28  11.3     26     156

Percentage of the requests served within a certain time (ms)
  50%     26
  66%     29
  75%     32
  80%     34
  90%     38
  95%     43
  98%     55
  99%     76
 100%    156 (longest request)
```