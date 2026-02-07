package com.ronnyBros;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class AppTest {

    @BeforeAll
    public static void setup() throws Exception {
        String[] args = {};
        LocalDynamoDB.main(args);
    }

    @Test
    public void shouldAnswerWithTrue() {
        assertTrue(true);
    }
}
