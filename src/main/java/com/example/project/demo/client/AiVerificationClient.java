package com.example.project.demo.client;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

/**
 * Sends text to the external AI service for a second verification pass.
 * If the call fails for any reason, falls back to whatever was passed in.
 */
@Component
public class AiVerificationClient {

    private static final Logger log = LoggerFactory.getLogger(AiVerificationClient.class);

    private final WebClient webClient;

    public AiVerificationClient(@Value("${ai.service.url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }

    public Mono<String> verify(String text) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder.path("/verify").queryParam("text", text).build())
            .retrieve()
            .bodyToMono(VerifyResponse.class)
            .map(VerifyResponse::cleaned)
            .onErrorResume(e -> {
                log.warn("AI verification failed, falling back to layer-1 result: {}", e.getMessage());
                return Mono.just(text);
            });
    }

    record VerifyResponse(String original, String cleaned, Object detections) {}
    
}
