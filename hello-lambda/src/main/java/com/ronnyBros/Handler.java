package com.ronnyBros;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayV2HTTPResponse;
import com.ronnyBros.model.Hello;
import com.ronnyBros.util.ApiResponseUtil;

import java.time.Instant;
import java.util.logging.Logger;

public class Handler implements RequestHandler<APIGatewayV2HTTPEvent, APIGatewayV2HTTPResponse> {

    static Logger log = Logger.getLogger(Handler.class.getName());
    @Override
    public APIGatewayV2HTTPResponse handleRequest(APIGatewayV2HTTPEvent event, Context context) {
        log.info("EVENT TYPE: " + event.getClass());

        String body = event.getBody() != null ? event.getBody() : "Empty body";
        log.info(String.format("body is %s", body));
        log.info(String.format("event is: %s", event));
        log.info(String.format("context is: %s", context));

        Hello hello = Hello.builder()
                .name("ronny")
                .timeISO(Instant.now().toString())
                .build();
        return ApiResponseUtil.jsonResponse(200, hello);
    }
}
