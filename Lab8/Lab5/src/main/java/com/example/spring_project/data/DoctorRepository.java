package com.example.spring_project.data;

import com.example.spring_project.entities.Doctor;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.stereotype.Repository;

@RepositoryRestResource(path = "doctors")
public interface DoctorRepository extends JpaRepository<Doctor, Long> {
}
