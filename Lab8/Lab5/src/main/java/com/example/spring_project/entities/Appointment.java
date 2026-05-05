package com.example.spring_project.entities;

import jakarta.persistence.*;
import lombok.Data;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;


@Entity
@Data
@Table(name = "appointment")
public class Appointment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "schedule_id", nullable = false)
    private AppointmentSchedule schedule;  // Связь с расписанием

    @NotNull(message = "Пожалуйста, введите имя")
    @Size(min = 2, max = 50, message = "Имя должно содержать от 2 до 50 символов")
    private String clientName;

    @NotNull(message = "Пожалуйста, введите фамилию")
    @Size(min = 2, max = 50, message = "Фамилия должна содержать от 2 до 50 символов")
    private String clientSurname;

    @NotNull(message = "Пожалуйста, введите номер телефона")
    @Pattern(regexp = "^(7|8)\\d{10}$", message = "Неверный формат номера телефона")
    private String clientPhone;

    @Size(max = 200, message = "Описание не может превышать 200 символов")
    private String clientDescription;
}
