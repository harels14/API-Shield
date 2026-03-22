package com.example.project.demo.controller;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.project.demo.client.AiVerificationClient;
import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.service.detection.SensitiveDataDetector;
import com.example.project.demo.service.tokenization.TextSanitizer;

@RestController
@RequestMapping
public class Controller {

    private final SensitiveDataDetector sensitiveDataDetector;
    private final TextSanitizer textSanitizer;
    private final AiVerificationClient aiVerificationClient;

    public Controller(SensitiveDataDetector sensitiveDataDetector, TextSanitizer textSanitizer, AiVerificationClient aiVerificationClient) {
        this.sensitiveDataDetector = sensitiveDataDetector;
        this.textSanitizer = textSanitizer;
        this.aiVerificationClient = aiVerificationClient;
    }

    @GetMapping("clean")
    public String cleanText(@RequestParam String text) {
        String layer1 = textSanitizer.sanitize(text);
        return aiVerificationClient.verify(layer1);
    }



    

    @GetMapping("detect")
    public String detectText(@RequestParam String text) {
        List<DetectionResult> results = sensitiveDataDetector.detect(text);
        return results.stream()
                .map(DetectionResult::toString)
                .collect(Collectors.joining(" - "));
    }

}
