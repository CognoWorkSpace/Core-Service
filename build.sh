docker build -t core-service:1.0 .
docker run -p 5000:5000 -it core-service:1.0