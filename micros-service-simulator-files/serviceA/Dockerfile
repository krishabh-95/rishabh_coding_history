FROM openjdk:11
ENV PORT 8090
EXPOSE 8090
ADD target/service-a.jar service-a.jar
ENTRYPOINT ["java","-jar","/service-a.jar"]