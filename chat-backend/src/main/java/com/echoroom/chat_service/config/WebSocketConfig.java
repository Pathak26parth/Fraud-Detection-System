package com.echoroom.chat_service.config;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Value("${frontend.urls}")
    private String[] frontendUrls;

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // for server sending message to client
        // example subscribing message
        config.enableSimpleBroker("/topic");

        // for server side controller to handle
        config.setApplicationDestinationPrefixes("/app");
    }


    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // connection is stabalished at /chat end point
        registry.addEndpoint("/chat")
                .setAllowedOrigins(frontendUrls)
                .withSockJS();
    }
}
