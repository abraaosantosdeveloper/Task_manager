CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE `tasks` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `description` varchar(200) not null,
    `status` ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `completed_at` DATETIME NULL
);

-- Insert tasks
INSERT INTO `tasks` (`title`, `description`, `completed_at`)
VALUES 
('Enviar relatório', 'Relatório mensal de vendas', '2025-11-03 15:30:00'),
('Comprar mantimentos', 'Ir ao supermercado no sábado', '2025-11-04 10:00')