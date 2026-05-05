package com.example.spring_project.service;

import com.example.spring_project.data.AppointmentScheduleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AppointmentScheduleService {
    @Autowired
    private AppointmentScheduleRepository appointmentScheduleRepository;

    public List<String> getAvailableTimesByDoctorId(int doctorId) {
        return appointmentScheduleRepository.findAvailableTimesByDoctorId(doctorId);
    }
}
