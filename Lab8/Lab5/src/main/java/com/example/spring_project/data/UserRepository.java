package com.example.spring_project.data;

import com.example.spring_project.entities.MyUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@RepositoryRestResource(path = "users")
public interface UserRepository extends JpaRepository<MyUser, Long> {
    Optional<MyUser> findByLogin(String login);
}
