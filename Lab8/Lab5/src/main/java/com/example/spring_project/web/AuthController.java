package com.example.spring_project.web;

import com.example.spring_project.entities.MyUser;
import com.example.spring_project.data.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@Controller
public class AuthController {

    private UserRepository repository;
    private PasswordEncoder passwordEncoder;

    @Autowired
    public AuthController(UserRepository repository) {
        this.repository = repository;
        passwordEncoder = new BCryptPasswordEncoder();
    }

    @PostMapping("/registration")
    public String registration(@ModelAttribute MyUser user, @RequestParam String confirm_password, Model model) {
        user.setRoles("user");

        Optional<MyUser> us = repository.findByLogin(user.getLogin());

        if (repository.findByLogin(user.getLogin()).isPresent()) {
            model.addAttribute("error", "Такой пользователь уже зарегистрирован!");
            return "registration";
        }

        if(!confirm_password.equals(user.getPassword())) {
            model.addAttribute("error", "Пароли не совпадают!");
            return "registration";
        }

        if(confirm_password.length() <= 5) {
            model.addAttribute("error", "Пароль слишком маленький!");
            return "registration";
        }

        addUser(user);
        return "login";
    }

    @GetMapping("/registration")
    public String getRegistrationForm() {
        return "registration";
    }

    @GetMapping("/login")
    public String login(@RequestParam(value = "error", required = false) String error, Model model) {
        if (error != null) {
            model.addAttribute("error", "Неверное имя пользователя или пароль!");
        }
        return "login";
    }

    public void addUser(MyUser user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        repository.save(user);
    }
}
