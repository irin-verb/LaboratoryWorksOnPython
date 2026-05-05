package com.example.spring_project;

import com.example.spring_project.data.DoctorRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.Arrays;

@SpringBootApplication
public class SpringProjectApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringProjectApplication.class, args);
	}

	@Bean
	public CommandLineRunner dataLoader(DoctorRepository repo) {
		return new CommandLineRunner() {
			@Override
			public void run(String... args) throws Exception {

			}
		};
	}

}
