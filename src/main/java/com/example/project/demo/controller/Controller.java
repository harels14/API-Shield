package com.example.project.demo.controller;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.service.detection.SensitiveDataDetector;
import com.example.project.demo.service.tokenization.TextSanitizer;

@RestController
@RequestMapping
public class Controller {

    private final SensitiveDataDetector sensitiveDataDetector;
    private final TextSanitizer textSanitizer;

    public Controller(SensitiveDataDetector sensitiveDataDetector, TextSanitizer textSanitizer) {
        this.sensitiveDataDetector = sensitiveDataDetector;
        this.textSanitizer = textSanitizer;
    }

    @GetMapping("clean")
    public String cleanText(@RequestParam String text) {
        return textSanitizer.sanitize(text);
    }

    

    @GetMapping("detect")
    public String detectText(@RequestParam String text) {
        List<DetectionResult> results = sensitiveDataDetector.detect(text);
        return results.stream()
                .map(DetectionResult::toString)
                .collect(Collectors.joining(" - "));
    }

}
