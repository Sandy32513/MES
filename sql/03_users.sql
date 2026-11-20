CREATE DATABASE IF NOT EXISTS mes_production_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

CREATE USER IF NOT EXISTS 'mes_admin'@'localhost' IDENTIFIED BY 't1f3BdLUxPjEiSYbezyn';
ALTER USER 'mes_admin'@'localhost' IDENTIFIED BY 't1f3BdLUxPjEiSYbezyn';
GRANT ALL PRIVILEGES ON mes_production_db.* TO 'mes_admin'@'localhost';

CREATE USER IF NOT EXISTS 'mes_admin'@'127.0.0.1' IDENTIFIED BY 't1f3BdLUxPjEiSYbezyn';
ALTER USER 'mes_admin'@'127.0.0.1' IDENTIFIED BY 't1f3BdLUxPjEiSYbezyn';
GRANT ALL PRIVILEGES ON mes_production_db.* TO 'mes_admin'@'127.0.0.1';

CREATE USER IF NOT EXISTS 'ignition_writer'@'localhost' IDENTIFIED BY 'KXVDu6qM1BStsboRTdhy';
ALTER USER 'ignition_writer'@'localhost' IDENTIFIED BY 'KXVDu6qM1BStsboRTdhy';
GRANT SELECT, INSERT, UPDATE ON mes_production_db.* TO 'ignition_writer'@'localhost';

CREATE USER IF NOT EXISTS 'ignition_writer'@'127.0.0.1' IDENTIFIED BY 'KXVDu6qM1BStsboRTdhy';
ALTER USER 'ignition_writer'@'127.0.0.1' IDENTIFIED BY 'KXVDu6qM1BStsboRTdhy';
GRANT SELECT, INSERT, UPDATE ON mes_production_db.* TO 'ignition_writer'@'127.0.0.1';

CREATE USER IF NOT EXISTS 'grafana_reader'@'localhost' IDENTIFIED BY 'L3ksWfrNZ0ogeiEqUt5y';
ALTER USER 'grafana_reader'@'localhost' IDENTIFIED BY 'L3ksWfrNZ0ogeiEqUt5y';
GRANT SELECT ON mes_production_db.* TO 'grafana_reader'@'localhost';

CREATE USER IF NOT EXISTS 'grafana_reader'@'127.0.0.1' IDENTIFIED BY 'L3ksWfrNZ0ogeiEqUt5y';
ALTER USER 'grafana_reader'@'127.0.0.1' IDENTIFIED BY 'L3ksWfrNZ0ogeiEqUt5y';
GRANT SELECT ON mes_production_db.* TO 'grafana_reader'@'127.0.0.1';

FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user WHERE user IN ('mes_admin', 'ignition_writer', 'grafana_reader');
