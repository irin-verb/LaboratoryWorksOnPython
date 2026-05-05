package com.example.spring_project.web;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class AppointmentSuccessController {

    @GetMapping("/appointment-success")
    public String appointmentSuccess() {
        return "appointment-success";
    }
}
