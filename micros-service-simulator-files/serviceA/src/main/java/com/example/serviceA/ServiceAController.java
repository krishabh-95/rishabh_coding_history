package com.example.serviceA;

import io.dapr.client.DaprClient;
import io.dapr.client.DaprClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ServiceAController
{
    String TOPIC_NAME = "test";
    String PUBSUB_NAME = "simulatorpubsub";

    @Value("${server.port}")
    int serverPort;

    @Value("${DAPR_HTTP_PORT}")
    int daprPort;

    @Value("${spring.application.name}")
    String appName;

    //publish a topic in redis pubsub broker
    @RequestMapping(path = "/hello")
    public String someMethod()
    {
        String str = "hello";
        DaprClient client = new DaprClientBuilder().build();
        client.publishEvent(
                PUBSUB_NAME,
                TOPIC_NAME,
                str).block();

        return "Message Delivered";
    }

    @RequestMapping(path = "/topic4")
    public String someMethodInA()
    {
        System.out.println("Service A has been invoked.");
        return "Service A has been invoked.";
    }
    @RequestMapping(path = "/get_topic")
    public String getTopicMethod()
    {
        System.out.println("Service A invoked from the method get_topic");
        return "Service A invoked from the method get_topic";
    }
}
