# otus_pro_04

## start sever
python3 httpd.py
python3 httpd.py -p 8080 -w 20

## get
curl -v http://localhost:8080/

## head
curl -v --head http://localhost:8080/

## post
curl --request POST --data '{"username":"xyz","password":"xyz"}' http://localhost:8080/

## test
python3 httptest.py

## browser test
http://localhost/httptest/wikipedia_russia.html 

## load test 
ab -n 50000 -c 100 -r http://localhost:8080/ 