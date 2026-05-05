CREATE TABLE doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    specialty VARCHAR(255) NOT NULL,
    experience INT
);

CREATE TABLE appointment_schedule (
    id INT PRIMARY KEY,
    doctor_id INT NOT NULL,
    date VARCHAR(255) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (doctor_id) REFERENCES doctor(id) ON DELETE CASCADE
);

CREATE TABLE users (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        login VARCHAR(50) NOT NULL,
        roles VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL,
        full_name VARCHAR(255) NOT NULL
);

INSERT INTO users (login,roles,password,email,full_name) VALUES
    ('vlad','user, admin','123','vlad@gmail.com','Vlad'),
    ('ivanov','user','111','ivanov@gmail.com','Ivan');


INSERT INTO doctor (full_name, specialty, experience) VALUES
    ('Машкова Светлана Васильевна', 'Гастроэрентолог', 15),
    ('Волков Владимир Сергеевич', 'Лор', 10),
    ('Котов Михаил Владимирович', 'Педиатр', 8);

INSERT INTO appointment_schedule (id,doctor_id, date, is_available) VALUES
    (1,1, '2024-10-15 9:00', TRUE),
    (2,1, '2024-10-16 14:30', TRUE),
    (3,2, '2024-10-15 10:00', TRUE),
    (4,2, '2024-10-17 15:00', FALSE),
    (5,3, '2024-10-18 10:00', TRUE),
    (6,3, '2024-10-19 14:00', TRUE),
    (7,3, '2024-10-20 8:30', TRUE);

CREATE TABLE appointment (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    schedule_id BIGINT NOT NULL,
    client_name VARCHAR(50) NOT NULL,
    client_surname VARCHAR(50) NOT NULL,
    client_phone VARCHAR(12) NOT NULL,
    client_description VARCHAR(200),
    FOREIGN KEY (schedule_id) REFERENCES appointment_schedule(id) ON DELETE CASCADE
);