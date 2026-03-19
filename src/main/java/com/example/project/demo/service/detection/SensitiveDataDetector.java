package com.example.project.demo.service.detection;
import org.springframework.stereotype.Service;
import com.example.project.demo.model.DetectionResult;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import com.example.project.demo.model.SensitiveDataType;





@Service
public class SensitiveDataDetector {

    private static final Pattern ISRAELI_ID_PATTERN = Pattern.compile("\\b\\d{9}\\b");
    private static final Pattern CREDIT_CARD_PATTERN = Pattern.compile("...");

    private static final Map<Pattern, SensitiveDataType> PATTERNS = Map.of(
    ISRAELI_ID_PATTERN, SensitiveDataType.ISRAELI_ID,
    CREDIT_CARD_PATTERN, SensitiveDataType.CREDIT_CARD);





    public List<DetectionResult> detect(String text) {
        List<DetectionResult> results = new ArrayList<>();
        for (Map.Entry<Pattern, SensitiveDataType> entry : PATTERNS.entrySet()) {
            results.addAll(detectByPattern(text, entry.getKey(), entry.getValue()));
        }

        return results;

    }


    private List<DetectionResult> detectByPattern(String text, Pattern pattern, SensitiveDataType type) {
        List<DetectionResult> results = new ArrayList<>();
        Matcher matcher = pattern.matcher(text);
        while (matcher.find()) {
            DetectionResult result = new DetectionResult(type, matcher.group(), matcher.start(), matcher.end());
            results.add(result);
        }

        return results;
    }





}