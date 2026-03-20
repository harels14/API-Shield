package com.example.project.demo.service.detection.validator;

public final class ValidateIsraeliID {

    public static boolean isValidIsraeliId(String id) {
        if (id == null || id.length() != 9) return false;

        return (LuhnAlgorithm(id));
        
    }

    private static boolean LuhnAlgorithm(String id) {  
        int sum = 0;
        for (int i = 0; i < 9; i++) {
            int digit = id.charAt(i) - '0';
            int step = digit * ((i % 2) + 1);
            sum += (step > 9) ? step - 9 : step;
        }
        
        return sum % 10 == 0;
    }
    
}
