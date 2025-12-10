-- Tabela para manter o banco de dados ativo
-- Usada pelo endpoint /api/keep-alive/ping para evitar que o banco "durma"

CREATE TABLE IF NOT EXISTS `dummy_data` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `last_ping` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `description` VARCHAR(255) DEFAULT 'Keep-alive ping data'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insere um registro inicial
INSERT INTO `dummy_data` (`is_active`, `description`) 
VALUES (TRUE, 'Database keep-alive record')
ON DUPLICATE KEY UPDATE `last_ping` = CURRENT_TIMESTAMP;
