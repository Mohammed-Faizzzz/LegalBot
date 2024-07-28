package com.example.LegalBot;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class QAController {
    private static final Logger logger = LoggerFactory.getLogger(QAController.class);

    @GetMapping("/")
    public String home() {
        return "index";
    }

    @PostMapping("/ask")
    public String ask(@RequestParam String question, Model model) {
        logger.info("Received question: " + question);
        String answer = getPythonScriptAnswer(question);
        logger.info("Generated answer: " + answer);
        model.addAttribute("question", question);
        model.addAttribute("answer", answer);
        return "result";
    }

    private String getPythonScriptAnswer(String question) {
        try {
            logger.info("Executing Python script");
            ProcessBuilder pb = new ProcessBuilder("python", "retrieval_mech/singlepred.py", question);
            pb.redirectErrorStream(true);
            pb.directory(new File(System.getProperty("user.dir")));
            Process p = pb.start();
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = in.readLine()) != null) {
                logger.info("Python output: " + line);
                output.append(line).append("\n");
            }
            String fullOutput = output.toString().trim();
            logger.info("Full Python output: " + fullOutput);
            return extractAnswer(fullOutput);
        } catch (Exception e) {
            logger.error("Error executing Python script", e);
            return "An error occurred while processing your question: " + e.getMessage();
        }
    }

    private String extractAnswer(String fullOutput) {
        String[] lines = fullOutput.split("\n");
        for (String line : lines) {
            if (line.startsWith("Final Answer:")) {
                return line.substring("Final Answer:".length()).trim();
            }
        }
        return "No answer found.";
    }
}