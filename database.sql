-- Task Manager Database Schema
CREATE DATABASE IF NOT EXISTS task_manager;
USE task_manager;

-- Users table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tasks table
CREATE TABLE IF NOT EXISTS `tasks` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `status` ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `completed_at` DATETIME NULL,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    INDEX idx_user_id (`user_id`),
    INDEX idx_status (`status`),
    INDEX idx_created_at (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dummy table for keep-alive (prevents database sleep)
CREATE TABLE IF NOT EXISTS `dummy_data` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `last_ping` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `description` VARCHAR(255) DEFAULT 'Keep-alive ping data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert initial dummy record
INSERT INTO `dummy_data` (`is_active`, `description`) 
VALUES (TRUE, 'Database keep-alive record');

-- Sample data (optional - for testing)
-- Note: Password is 'password123' hashed with bcrypt
-- INSERT INTO `users` (`email`, `password`, `name`)
-- VALUES ('demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIFQN8mXqO', 'Demo User');