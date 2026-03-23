package com.example.project.demo.controller;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.project.demo.client.AiVerificationClient;
import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.service.detection.SensitiveDataDetector;
import com.example.project.demo.service.tokenization.TextSanitizer;

/**
 * Entry point for the API. Two endpoints: /clean runs the full sanitization
 * pipeline (regex + AI verification), /detect just reports what was found.
 */
@RestController
@RequestMapping
public class Controller {

    private static final Logger log = LoggerFactory.getLogger(Controller.class);

    private final SensitiveDataDetector sensitiveDataDetector;
    private final TextSanitizer textSanitizer;
    private final AiVerificationClient aiVerificationClient;

    public Controller(SensitiveDataDetector sensitiveDataDetector, TextSanitizer textSanitizer, AiVerificationClient aiVerificationClient) {
        this.sensitiveDataDetector = sensitiveDataDetector;
        this.textSanitizer = textSanitizer;
        this.aiVerificationClient = aiVerificationClient;
    }

    // main entry
    @GetMapping("clean")
    public ResponseEntity<String> cleanText(@RequestParam(required = false) String text) {
        if (text == null || text.isBlank()) {
            log.warn("Received empty or null text on /clean");
            return ResponseEntity.badRequest().body("text is required");
        }
        log.info("Sanitizing text of length {}", text.length());
        String layer1 = textSanitizer.sanitize(text);
        String result = aiVerificationClient.verify(layer1);
        log.info("Sanitization complete");
        return ResponseEntity.ok(result);
    }

    @GetMapping("detect")
    public ResponseEntity<?> detectText(@RequestParam(required = false) String text) {
        if (text == null || text.isBlank()) {
            log.warn("Received empty or null text on /detect");
            return ResponseEntity.badRequest().body("text is required");
        }
        log.info("Detecting PII in text of length {}", text.length());
        List<DetectionResult> results = sensitiveDataDetector.detect(text);
        log.info("Detection found {} result(s)", results.size());
        return ResponseEntity.ok(results);
    }

}
