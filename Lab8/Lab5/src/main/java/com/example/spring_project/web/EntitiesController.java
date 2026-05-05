package com.example.spring_project.web;

import com.example.spring_project.entities.Appointment;
import com.example.spring_project.data.AppointmentRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class EntitiesController {

    private final AppointmentRepository appointmentRepository;

    public EntitiesController(AppointmentRepository appointmentRepository){
        this.appointmentRepository = appointmentRepository;
    }

    @GetMapping("/appointments")
    public String appointments(Model model) {
        List<Appointment> appointmentList = appointmentRepository.findAll();
        model.addAttribute("appointments", appointmentList);
        return "appointments";
    }
}
