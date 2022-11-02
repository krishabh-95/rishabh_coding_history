FROM openjdk:11
ENV PORT 8080
EXPOSE 8080
ADD target/service-b.jar service-b.jar
ENTRYPOINT ["java","-jar","/service-b.jar"]


