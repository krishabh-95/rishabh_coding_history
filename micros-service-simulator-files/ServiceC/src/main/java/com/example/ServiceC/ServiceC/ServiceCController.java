package com.example.ServiceC.ServiceC;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import io.dapr.Topic;
import io.dapr.client.domain.CloudEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

@RestController
public class ServiceCController
{
    private static final Logger logger = LoggerFactory.getLogger(ServiceCController.class);

    RestTemplate restTemplate = new RestTemplate();

    @Value("${server.port}")
    int serverPort;

    @Value("${DAPR_HTTP_PORT}")
    int daprPort;

    @Value("${spring.application.name}")
    String appName;

    /*
    @Topic(name = "test", pubsubName = "simulatorpubsub")
    @PostMapping(path = "/test")
    public ResponseEntity<String> getCheckout(@RequestBody(required = false)  CloudEvent<String> cloudEvent) throws IOException, InterruptedException {
        logger.info("Received :"  + cloudEvent.getData());
        System.out.println("Service C has been triggered.");
        return ResponseEntity.ok("SUCCESS");

    } */

    @GetMapping(path = "/hello-there")
    public String callFromB()
    {
        return "hello there";
    }

    @RequestMapping(path = "/test")
    public String someMethod()
    {
        System.out.println("C has been invoked");
        return "Service C has been invoked.";
    }

    @RequestMapping(path = "/topic3")
    public String invokeTopic3() throws IOException
    {
        System.out.println("Going to invoke service A");
        String url= "http://localhost:"+daprPort+"/v1.0/invoke/service-a/method/get_topic";
        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("GET");
        con.setRequestProperty("User-Agent", "Mozilla/5.0");

        if(con.getResponseCode()== HttpURLConnection.HTTP_OK)
        {
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String line;
            StringBuffer response = new StringBuffer();

            while ((line = in.readLine()) != null) {
                response.append(line);
            }
            in.close();
            System.out.println(response.toString());
            return response.toString();
        }
        else {
            System.out.println("Error occurred while invoking service A");
            return "Error occurred while invoking service A";
        }
    }
}
