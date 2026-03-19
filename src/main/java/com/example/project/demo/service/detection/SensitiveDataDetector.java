package com.example.project.demo.service.detection;
import org.springframework.stereotype.Service;
import com.example.project.demo.model.DetectionResult;
import java.util.List;
import java.util.ArrayList;



@Service
public class SensitiveDataDetector {


    public List<DetectionResult> detect(String text) {
        return new ArrayList<>();

    }



}