CREATE DATABASE blog;
USE blog;
CREATE TABLE users
(
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255)           NOT NULL UNIQUE,
    password VARCHAR(255)           NOT NULL,
    role     ENUM ('admin', 'user') NOT NULL DEFAULT 'user'
);
CREATE TABLE posts
(
    id         INT AUTO_INCREMENT PRIMARY KEY,
    title      VARCHAR(255) NOT NULL,
    content    TEXT         NOT NULL,
    author     VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);