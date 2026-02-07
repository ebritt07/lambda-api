package org.example;

import software.amazon.dynamodb.services.local.main.ServerRunner;
import software.amazon.dynamodb.services.local.server.DynamoDBProxyServer;


public class Main {
    public static void main(String[] args) {
        try {
            int DEFAULT_PORT = 8001;
            String port = String.valueOf(DEFAULT_PORT);
            if(args.length > 0) {
                port = args[0];
            }

            final String[] localArgs = {"-inMemory", "-port", port};
            System.out.println("Starting DynamoDB Local...");
            DynamoDBProxyServer server = ServerRunner.createServerFromCommandLineArgs(localArgs);
            server.start();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}