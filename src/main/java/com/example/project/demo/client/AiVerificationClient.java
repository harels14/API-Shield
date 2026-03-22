package com.example.project.demo.client;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class AiVerificationClient {

    private final WebClient webClient;

    public AiVerificationClient(@Value("${ai.service.url}") String baseUrl) {
        this.webClient = WebClient.builder().baseUrl(baseUrl).build();
    }
    
    public String verify(String text) {
        return webClient.get()
            .uri(uriBuilder -> uriBuilder.path("/verify").queryParam("text", text).build())
            .retrieve()
            .bodyToMono(VerifyResponse.class)
            .map(VerifyResponse::cleaned)
            .onErrorReturn(text)  
            .block();
    }

    record VerifyResponse(String original, String cleaned, Object detections) {}
    
}
