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

    /**
     * Detects all sensitive data in the text and replaces each match with
     * the placeholder defined by its {@link com.example.project.demo.model.SensitiveDataType}.
     * Replacements are applied from end to start to keep indices stable.
     *
     * @param text the original text
     * @return the sanitized text with sensitive values replaced by their type placeholder
     */
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
