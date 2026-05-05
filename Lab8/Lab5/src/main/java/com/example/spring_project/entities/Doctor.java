package com.example.spring_project.entities;

import jakarta.persistence.*;
import lombok.Data;

import java.util.List;

@Entity
@Data
@Table(name="doctor")
public class Doctor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    private String fullName;

    private String specialty;

    private int experience;

    @OneToMany(mappedBy = "doctor", cascade = CascadeType.ALL)
    private List<AppointmentSchedule> schedule;
}
