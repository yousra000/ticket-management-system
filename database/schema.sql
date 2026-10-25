-- Run once from the project root:
--   mysql -u root -p -e "source database/schema.sql"
-- The password below must match DATABASE_URL in your .env file.
-- Change it for anything beyond local development.

CREATE DATABASE IF NOT EXISTS ticketdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'ticket_user'@'localhost' IDENTIFIED BY 'ChangeMe_Local_123';
CREATE USER IF NOT EXISTS 'ticket_user'@'127.0.0.1' IDENTIFIED BY 'ChangeMe_Local_123';

GRANT ALL PRIVILEGES ON ticketdb.* TO 'ticket_user'@'localhost';
GRANT ALL PRIVILEGES ON ticketdb.* TO 'ticket_user'@'127.0.0.1';
FLUSH PRIVILEGES;

USE ticketdb;

CREATE TABLE IF NOT EXISTS tickets (
  id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
  title       VARCHAR(200) NOT NULL,
  description TEXT NULL,
  status      VARCHAR(20)  NOT NULL DEFAULT 'open',
  priority    VARCHAR(20)  NOT NULL DEFAULT 'medium',
  assignee    VARCHAR(100) NULL,
  created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  INDEX idx_tickets_status (status),
  CONSTRAINT ck_tickets_status CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
  CONSTRAINT ck_tickets_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
