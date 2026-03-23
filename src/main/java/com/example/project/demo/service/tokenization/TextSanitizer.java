package com.example.project.demo.service.tokenization;

import java.util.Comparator;
import java.util.List;

import org.springframework.stereotype.Service;

import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.service.detection.SensitiveDataDetector;

/**
 * Sanitizes text by replacing sensitive data with type-specific placeholders.
 * Example: "054-3982092" → "[PHONE_NUMBER]"
 */
@Service
public class TextSanitizer {

    private final SensitiveDataDetector detector;

    public TextSanitizer(SensitiveDataDetector detector) {
        this.detector = detector;
    }

    /** Replaces all detected PII with its placeholder. Works end-to-start so indices stay valid. */
    public String sanitize(String text) {
        if (text == null || text.isBlank()) {
            return text;
        }

        List<DetectionResult> detections = detector.detect(text);

        // Sort descending by startIndex so replacements don't shift subsequent indices
        detections.sort(Comparator.comparingInt(DetectionResult::getStartIndex).reversed());

        StringBuilder sb = new StringBuilder(text);
        for (DetectionResult result : detections) {
            String placeholder = result.getType().getPlaceholder();
            sb.replace(result.getStartIndex(), result.getEndIndex(), placeholder);
        }

        return sb.toString();
    }
}
