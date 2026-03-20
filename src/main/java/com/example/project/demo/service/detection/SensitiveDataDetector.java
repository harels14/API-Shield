package com.example.project.demo.service.detection;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.stereotype.Service;

import com.example.project.demo.model.DetectionResult;
import com.example.project.demo.model.SensitiveDataType;
import com.example.project.demo.service.detection.validator.ValidateIsraeliID;


/**
 * Scans text and looks for sensitive data like Israeli IDs and credit card numbers.
 * Each data type has its own regex pattern defined as a constant.
 */
@Service
public class SensitiveDataDetector {

    private static final Pattern ISRAELI_ID_PATTERN = Pattern.compile("(?<!\\d)\\d{9}(?!\\d)");
    private static final Pattern CREDIT_CARD_PATTERN = Pattern.compile("(?<!\\d)(?:\\d{4}[ -]?){3}\\d{4}(?!\\d)");
    private static final Pattern PHONE_NUMBER_PATTERN = Pattern.compile("(?<!\\d)(?:\\+972[- ]?|0)(?:[23489]|5[0-9]|7[0-9])[- ]?\\d{7}(?!\\d)");
    private static final Pattern EMAIL_PATTERN = Pattern.compile("\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b");


    private static final Map<Pattern, SensitiveDataType> PATTERNS = Map.of(
    ISRAELI_ID_PATTERN, SensitiveDataType.ISRAELI_ID,
    CREDIT_CARD_PATTERN, SensitiveDataType.CREDIT_CARD,
    PHONE_NUMBER_PATTERN, SensitiveDataType.PHONE_NUMBER,
    EMAIL_PATTERN, SensitiveDataType.EMAIL);



    /**
     * Takes a text string and returns all matches found across every pattern.
     * Each result includes the type, the matched value, and where it was found in the text.
     * Returns an empty list if nothing was found.
     *
     * @param text the text to scan
     * @return list of detection results
     */
    public List<DetectionResult> detect(String text) {
        List<DetectionResult> results = new ArrayList<>();
        for (Map.Entry<Pattern, SensitiveDataType> entry : PATTERNS.entrySet()) {
            results.addAll(detectByPattern(text, entry.getKey(), entry.getValue()));
        }

        return results;

    }

    /**
     * Runs a single regex pattern against the text and collects all matches.
     * For each match it records the sensitive data type, the matched string, and the start/end positions.
     *
     * @param text    the text to scan
     * @param pattern the regex pattern to apply
     * @param type    the sensitive data type this pattern looks for
     * @return list of matches found for this pattern
     */
    private List<DetectionResult> detectByPattern(String text, Pattern pattern, SensitiveDataType type) {
        List<DetectionResult> results = new ArrayList<>();
        Matcher matcher = pattern.matcher(text);
        while (matcher.find()) {
            if (type == SensitiveDataType.ISRAELI_ID) {
                if (!ValidateIsraeliID.isValidIsraeliId(matcher.group())) continue;
            }
            
            DetectionResult result = new DetectionResult(type, matcher.group(), matcher.start(), matcher.end());
            results.add(result);
        }

        return results;
    }

}
