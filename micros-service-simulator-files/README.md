We can simulate a service to service invocation with a basic REST api

Both services are running on differnet ports - ServiceA on port 8090 and ServiceB on 8080

How To:

1.Clone the repo

2.start both the servers up 

3.url for ServiceA - http://localhost:8090/helloworld/serviceA

4.Stop running serviceB and observe serviceA call fails 

NOTE: Theres a docker file in both the folders to play around with as well


Service A dapr command : dapr run --app-id service-a --app-port 8090 --dapr-http-port 3501 --components-path ../components -- java -jar target/service-a.jar


Service B dapr command : dapr run --app-id service-b --app-port 8080 --dapr-http-port 3500 --components-path ../components -- java -jar target/service-b.jar


Service C dapr command : dapr run --app-id service-c --app-port 8091 --dapr-http-port 3502 --components-path ../components -- java -jar target/service-c.jar
