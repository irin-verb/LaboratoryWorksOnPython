package com.example.spring_project.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@EnableConfigurationProperties(DataBaseConfig.class)
@Profile("prod")
public class ProdDataBaseConfig {

    @Bean
    public DataBaseConfig databaseConfig() {
        return new DataBaseConfig();
    }
}
