CREATE DATABASE IF NOT EXISTS club_robot;
USE club_robot;
-- GRANT ALL ON club_robot.* TO 'changyuf'@'%';

CREATE TABLE IF NOT EXISTS qq_account(
	uin VARCHAR(40) CHARACTER SET utf8 DEFAULT NULL, 
	qq VARCHAR(40) CHARACTER SET utf8 NOT NULL,
	nick_name VARCHAR(60) CHARACTER SET utf8 DEFAULT NULL,
	gender  VARCHAR(4) CHARACTER SET utf8 DEFAULT NULL,
	balance int,
	club_level   int,
	activity_times  int,
	accumulate_points int,
	card varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
	comments VARCHAR(200) COLLATE utf8_unicode_ci DEFAULT NULL,
	other_comments varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
	PRIMARY KEY (qq)
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
	
CREATE TABLE IF NOT EXISTS activities(
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	title VARCHAR(100) CHARACTER SET utf8 NOT NULL, 
	discription VARCHAR(300) CHARACTER SET utf8 DEFAULT NULL,
	activity_position VARCHAR(80) CHARACTER SET utf8 NOT NULL,
	start_time  DATETIME  NOT NULL,
	stop_time DATETIME NOT NULL,
	price_male INT NOT NULL,
	price_femal  INT NOT NULL,
	max_participants  INT NOT NULL,
	dead_line  DATETIME NOT NULL,
	organiser  VARCHAR(100) CHARACTER SET utf8 NOT NULL,
	organiser_phone  VARCHAR(100) CHARACTER SET utf8 DEFAULT NULL	
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
	

	


Participants