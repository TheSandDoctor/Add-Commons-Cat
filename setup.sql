CREATE DATABASE commons_task3_run;
use commons_task3_run;
CREATE TABLE `runs` (
	`title` TEXT,
	`date_added` VARCHAR(255)
);
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON commons_task3_run . * TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
