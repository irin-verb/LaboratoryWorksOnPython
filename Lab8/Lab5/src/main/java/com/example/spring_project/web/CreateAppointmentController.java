package com.example.spring_project.web;

import com.example.spring_project.entities.Appointment;
import com.example.spring_project.service.AppointmentScheduleService;
import com.example.spring_project.entities.Doctor;
import com.example.spring_project.data.AppointmentRepository;
import com.example.spring_project.data.DoctorRepository;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

import java.util.List;


@Slf4j
@Controller
@RequestMapping("/appointment")
public class CreateAppointmentController {

    private final AppointmentRepository appointmentRepository;
    private final DoctorRepository doctorRepository;

    @Autowired
    private AppointmentScheduleService appointmentScheduleService;

    @Autowired
    public CreateAppointmentController(AppointmentRepository appointmentRepository, DoctorRepository doctorRepository) {
        this.appointmentRepository = appointmentRepository;
        this.doctorRepository = doctorRepository;
    }

    @ModelAttribute
    public void addDoctorsToModel(Model model) {
        List<Doctor> doctors = doctorRepository.findAll();
        model.addAttribute("doctors", doctors);
    }

    @GetMapping
    public String showDesignForm(Model model) {
        model.addAttribute("appointment", new Appointment());

        return "appointment";
    }

    @GetMapping("/available-times/{doctorId}")
    @ResponseBody
    public List<String> getAvailableTimes(@PathVariable int doctorId) {
        return appointmentScheduleService.getAvailableTimesByDoctorId(doctorId);
    }

    @PostMapping
    public String createAppointment(@Valid @ModelAttribute("appointment") Appointment appointment, BindingResult result, Model model) {

        if (result.hasErrors()) {
            return "appointment";
        }

        appointment.getSchedule().setId(1L);
        appointmentRepository.insertAppointment(appointment.getSchedule().getId(),appointment.getClientName(),
                appointment.getClientSurname(),appointment.getClientPhone(),appointment.getClientDescription());
        
        return "redirect:/appointment-success";
    }

}
