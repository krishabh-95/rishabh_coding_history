FROM openjdk:11
ENV PORT 8091
EXPOSE 8091
ADD target/service-c.jar service-c.jar
ENTRYPOINT ["java","-jar","/service-c.jar"]