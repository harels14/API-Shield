package com.example.project.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import com.example.project.demo.service.detection.SensitiveDataDetector;


@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@Bean
	public CommandLineRunner test(SensitiveDataDetector detector) {
        return args -> {
            var results = detector.detect("""
                                           Hello Team,\r
                                          \r
                                          Below are the details for opening a business account for our SaaS platform.\r
                                          \r
                                          Primary Contact Information:\r
                                          Name: David Cohen. ID Number: 123456782.\r
                                          Please note that we also have a partner from abroad with passport number 987654321, please update the system.\r
                                          Do not confuse this with our company registration number which is 512345678 (even though it's also 9 digits).\r
                                          \r
                                          Contact Phone Numbers:\r
                                          Personal Mobile: 052-1234567.\r
                                          Office landline in Ra'anana: 09-7654321.\r
                                          During vacations abroad (like when I am in Budapest or Vienna) I am available at the international number: +972549876543.\r
                                          Please do not call the old number 05-1234567 (it is invalid, missing a digit).\r
                                          \r
                                          Email Addresses:\r
                                          Main contact email: my-name.last_name@company.co.il.\r
                                          Secondary system email (for development): admin+dev@yedabot.com.\r
                                          I noticed clients trying to register with invalid emails like user@domain or just @gmail.com, so do not send any billing info there.\r
                                          \r
                                          Payment Methods for Monthly Billing:\r
                                          Mastercard ending in 9012. The full number to enter in the system is 5326-1111-2222-3333.\r
                                          We also tried a Visa with no dashes at all: 4""" //
            );
            results.forEach(System.out::println);
        };
    }

}
