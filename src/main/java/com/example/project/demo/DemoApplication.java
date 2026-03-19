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
            var results = detector.detect("תשלום עבור ת.ז 123456782 בסך 500 שקל");
            results.forEach(System.out::println);
        };
    }

}
