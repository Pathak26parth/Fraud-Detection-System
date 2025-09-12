package com.echoroom.chat_service.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;

@Service
public class SpamDetectionService {

    @Value("${spam.detection.api.url:http://localhost:8001}")
    private String spamDetectionApiUrl;

    private final WebClient webClient;

    public SpamDetectionService() {
        this.webClient = WebClient.builder()
                .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(1024 * 1024))
                .build();
    }

    public SpamDetectionResult detectSpam(String messageContent) {
        try {
            SpamDetectionRequest request = new SpamDetectionRequest(messageContent);
            
            SpamDetectionResponse response = webClient.post()
                    .uri(spamDetectionApiUrl + "/predict")
                    .body(Mono.just(request), SpamDetectionRequest.class)
                    .retrieve()
                    .bodyToMono(SpamDetectionResponse.class)
                    .timeout(Duration.ofSeconds(5))
                    .onErrorReturn(new SpamDetectionResponse(0.0))
                    .block();

            if (response != null) {
                double spamLevel = response.getSpamLevel();
                boolean isSpam = spamLevel > 0.5;
                return new SpamDetectionResult(spamLevel, isSpam);
            }
            
            return new SpamDetectionResult(0.0, false);
        } catch (Exception e) {
            // Log error and return safe default
            System.err.println("Error calling spam detection API: " + e.getMessage());
            return new SpamDetectionResult(0.0, false);
        }
    }

    public static class SpamDetectionRequest {
        private String text;

        public SpamDetectionRequest() {}

        public SpamDetectionRequest(String text) {
            this.text = text;
        }

        public String getText() {
            return text;
        }

        public void setText(String text) {
            this.text = text;
        }
    }

    public static class SpamDetectionResponse {
        private double spamLevel;

        public SpamDetectionResponse() {}

        public SpamDetectionResponse(double spamLevel) {
            this.spamLevel = spamLevel;
        }

        public double getSpamLevel() {
            return spamLevel;
        }

        public void setSpamLevel(double spamLevel) {
            this.spamLevel = spamLevel;
        }
    }

    public static class SpamDetectionResult {
        private final double spamLevel;
        private final boolean isSpam;

        public SpamDetectionResult(double spamLevel, boolean isSpam) {
            this.spamLevel = spamLevel;
            this.isSpam = isSpam;
        }

        public double getSpamLevel() {
            return spamLevel;
        }

        public boolean isSpam() {
            return isSpam;
        }
    }
}
