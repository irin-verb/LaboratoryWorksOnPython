package com.example.spring_project.data;

import com.example.spring_project.entities.Appointment;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.data.rest.webmvc.RepositoryRestController;
import org.springframework.stereotype.Repository;

@RepositoryRestResource(path = "appointments")
public interface AppointmentRepository extends JpaRepository<Appointment, Long> {
    @Modifying
    @Transactional
    @Query(value = "INSERT INTO Appointment (schedule_id, client_name, client_surname, client_phone, client_description) VALUES (:schedule_id, :client_name, :client_surname,:client_phone,:client_description)", nativeQuery = true)
    void insertAppointment(@Param("schedule_id") Long schedule_id, @Param("client_name") String client_name, @Param("client_surname") String client_surname, @Param("client_phone") String client_phone, @Param("client_description") String client_description);
}
