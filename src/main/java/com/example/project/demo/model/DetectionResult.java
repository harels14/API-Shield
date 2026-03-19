package com.example.project.demo.model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class DetectionResult {
    private SensitiveDataType type;
    private String originalValue;
    private int startIndex;
    private int endIndex;
}
