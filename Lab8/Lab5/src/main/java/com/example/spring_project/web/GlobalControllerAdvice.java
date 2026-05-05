package com.example.spring_project.web;

import com.example.spring_project.service.MyUserDetails;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

@ControllerAdvice
public class GlobalControllerAdvice {

    @ModelAttribute("authenticatedUsername")
    public String addAuthenticatedUsername() {
        return getAuthenticatedUsername();
    }

    private String getAuthenticatedUsername() {
        Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        if (principal instanceof MyUserDetails) {
            return ((MyUserDetails) principal).getFullName();
        }
        return null; // Если пользователь не аутентифицирован
    }
}
