package com.example.legalbot.controller;

import com.example.legalbot.service.LegalBotService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class LegalBotController {

    @Autowired
    private LegalBotService legalBotService;

    @GetMapping("/")
    public String index() {
        return "index";
    }

    @PostMapping("/query")
    public String query(@RequestParam String question, Model model) {
        String answer = legalBotService.getAnswer(question);
        model.addAttribute("question", question);
        model.addAttribute("answer", answer);
        return "index";
    }
}
