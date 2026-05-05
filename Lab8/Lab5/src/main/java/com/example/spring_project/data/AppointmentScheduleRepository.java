package com.example.spring_project.data;

import com.example.spring_project.entities.AppointmentSchedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AppointmentScheduleRepository extends JpaRepository<AppointmentSchedule, Long> {
    @Query("SELECT a.date FROM AppointmentSchedule a WHERE a.doctor.id = :doctorId AND a.isAvailable = TRUE")
    List<String> findAvailableTimesByDoctorId(@Param("doctorId") int doctorId);
}
