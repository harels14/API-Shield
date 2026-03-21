package com.example.project.demo.model;

public enum SensitiveDataType {
    ISRAELI_ID("[ISRAELI_ID]"),
    CREDIT_CARD("[CREDIT_CARD]"),
    PHONE_NUMBER("[PHONE_NUMBER]"),
    EMAIL("[EMAIL]");

    private final String placeholder;

    SensitiveDataType(String placeholder) {
        this.placeholder = placeholder;
    }

    public String getPlaceholder() {
        return placeholder;
    }
}