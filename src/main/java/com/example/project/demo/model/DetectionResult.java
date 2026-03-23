package com.example.project.demo.model;

import lombok.AllArgsConstructor;
import lombok.Data;

/** One detected match: the PII type, the raw value, and its position in the original text. */
@Data
@AllArgsConstructor
public class DetectionResult {
    private SensitiveDataType type;
    private String originalValue;
    private int startIndex;
    private int endIndex;
}
