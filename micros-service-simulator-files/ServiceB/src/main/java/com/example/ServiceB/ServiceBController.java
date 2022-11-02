package com.example.ServiceB;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

@RestController
@RequestMapping
public class ServiceBController
{

    private static final Logger logger = LoggerFactory.getLogger(ServiceBController.class);
    RestTemplate restTemplate = new RestTemplate();

    @Value("${server.port}")
    int serverPort;

    @Value("${DAPR_HTTP_PORT}")
    int daprPort;

    @Value("${spring.application.name}")
    String appName;

    /*
    subscription model created programmatically,
    subscribes to a topic which is published by service A
    and calls method callServiceC() after the message from service A is received
    Topic name = test
    pubsubname = simulatorpubsub
    route = /test
*/
/*
    @Topic(name = "test", pubsubName = "simulatorpubsub")
    @PostMapping(path = "/test")
    public ResponseEntity<String> getCheckout(@RequestBody(required = false)  CloudEvent<String> cloudEvent) throws IOException, InterruptedException {
        logger.info("Received :"  + cloudEvent.getData());
        //callServiceC();
        System.out.println("Service B has been triggered.");
        return ResponseEntity.ok("SUCCESS");

    }*/
/*
    @Topic(name = "dependent_topic", pubsubName = "b_calls_c")
    @PostMapping(path="/dependent_test")
    public ResponseEntity<String> invokeServiceC(@RequestBody(required = false)  CloudEvent<String> cloudEvent) throws IOException, InterruptedException
    {
        logger.info("Received :"+cloudEvent.getData());
        System.out.println("Going to invoke service C");
        String url= "http://localhost:3502/v1.0/invoke/service-c/method/test";
        RestTemplate temp = new RestTemplate();
        String result = restTemplate.getForObject(url, String.class);
        System.out.println(result);
        return ResponseEntity.ok("SUCCESS");
    }*/

    @RequestMapping(path = "/test")
    public String someMethod()
    {
        System.out.println("B has been invoked.");
        return "Service B has been invoked.";
    }

    @RequestMapping(path = "/dependent_topic")
    public String someMethodFromB() throws IOException
    {
        System.out.println("Going to invoke service C");
        String url= "http://localhost:"+daprPort+"/v1.0/invoke/service-c/method/test";
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
            System.out.println("Service C invoked successfully...");
            return response.toString();
        }
        else {
            System.out.println("Error occurred while invoking service C");
            return "Error occurred while invoking service C";
        }
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
            System.out.println("Service A invoked successfully...");
            return response.toString();
        }
        else {
            System.out.println("Error occurred while invoking service A");
            return "Error occurred while invoking service A";
        }
        /*RestTemplate temp = new RestTemplate();
        String result = restTemplate.getForObject(url, String.class);
        System.out.println(result);
        return result;*/
    }

    /*
    method to simulate an api call to service C
    the string uri can be changed accordignly,
    currently it is calling service - C "/hello-there" api from port 3501 , which is service A's port

     */
    public void callServiceC() throws InterruptedException, IOException {
        System.out.println("Server port is "+serverPort);
        final String uri = "http://localhost:"+daprPort+"/v1.0/invoke/service-c/method/hello-there";
        URL obj = new URL(uri);
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
        }
        else {
            System.out.println("Service C is not responding");
        }
    }

    @RequestMapping(path = "/delayed_topic")
    public String someMethodFromClassB() throws IOException, InterruptedException
    {
        //In this method we invoke service C after pausing the thread for 10 seconds
        Thread.sleep(10000);
        String uri = "http://localhost:"+daprPort+"/v1.0/invoke/service-c/method/hello-there";
        URL obj = new URL(uri);
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
            System.out.println("Service C has been invoked. Its response is "+response.toString());
            return response.toString();
        }
        else {
            System.out.println("Service C is not responding");
            return "Service C is not responding";
        }
    }
}
