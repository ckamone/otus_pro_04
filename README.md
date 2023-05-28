# otus_pro_04

## start sever
python3 httpd.py

## get
curl -v http://localhost:8080/

## head
curl -v --head http://localhost:8080/

## post
curl --request POST --data '{"username":"xyz","password":"xyz"}' http://localhost:8080/