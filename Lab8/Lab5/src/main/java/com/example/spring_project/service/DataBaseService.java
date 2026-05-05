package com.example.spring_project.service;

import com.example.spring_project.config.DataBaseConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DataBaseService {

    private final DataBaseConfig databaseConfig;

    @Autowired
    public DataBaseService(DataBaseConfig databaseConfig) {
        this.databaseConfig = databaseConfig;
    }
}
