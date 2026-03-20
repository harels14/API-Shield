package com.example.project.demo.controller;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.web.bind.annotation.*;
import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.service.detection.SensitiveDataDetector;

@RestController
@RequestMapping
public class Controller {

    private final SensitiveDataDetector sensitiveDataDetector;

    public Controller(SensitiveDataDetector sensitiveDataDetector) {
        this.sensitiveDataDetector = sensitiveDataDetector;
    }

    @GetMapping("clean")
    public String cleanText(@RequestParam String text) {
        List<DetectionResult> results = sensitiveDataDetector.detect(text);
        return results.stream()
                .map(DetectionResult::toString)
                .collect(Collectors.joining(" - "));
    }

}
