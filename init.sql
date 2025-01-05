CREATE DATABASE IF NOT EXISTS visitor_counter;

CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT ALL PRIVILEGES ON visitor_counter.* TO 'app_user'@'%';
FLUSH PRIVILEGES;

USE visitor_counter;

CREATE TABLE IF NOT EXISTS visitors (
    id INT PRIMARY KEY,
    count INT DEFAULT 0
);

INSERT INTO visitors (id, count) VALUES (1, 0) 
ON DUPLICATE KEY UPDATE id=id;