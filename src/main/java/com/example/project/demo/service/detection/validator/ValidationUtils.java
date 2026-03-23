package com.example.project.demo.service.detection.validator;

/**
 * Format and checksum validation to cut down false positives from the regex patterns.
 */
public final class ValidationUtils {

    public static boolean isValidIsraeliId(String id) {
        if (id == null || !id.matches("\\d{9}")) return false;
        return LuhnAlgorithm(id);
    }

    public static boolean isValidCreditCard(String card) {
        String cleanCard = card.replaceAll("[\\s-]", "");
        if (cleanCard.length() < 13 || cleanCard.length() > 19) return false;
        return LuhnAlgorithm(cleanCard);
    }


    // Luhn checksum: alternate digits are doubled from the right, sum must be divisible by 10
    private static boolean LuhnAlgorithm(String number) {
        int sum = 0;
        boolean alternate = false;
        for (int i = number.length() - 1; i >= 0; i--) {
            int n = Integer.parseInt(number.substring(i, i + 1));
            if (alternate) {
                n *= 2;
                if (n > 9) n -= 9;
            }
            sum += n;
            alternate = !alternate;
        }
        return (sum % 10 == 0);
    }
    
}
