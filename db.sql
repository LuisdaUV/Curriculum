-- Crear base de datos y tabla para almacenar mensajes de visitantes
CREATE DATABASE IF NOT EXISTS cv_site CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cv_site;

CREATE TABLE IF NOT EXISTS guestbook (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(190) NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
