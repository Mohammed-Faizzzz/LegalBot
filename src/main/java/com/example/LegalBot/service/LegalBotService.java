package com.example.legalbot.service;

import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@Service
public class LegalBotService {

    public String getAnswer(String question) {
        try {
            ProcessBuilder pb = new ProcessBuilder("python", "python/qa_model.py", question);
            pb.redirectErrorStream(true);  // Redirect errors to the input stream
            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder result = new StringBuilder();
            String line;

            while ((line = reader.readLine()) != null) {
                result.append(line);
            }

            return result.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error: " + e.getMessage();
        }
    }
}
