CREATE DATABASE IF NOT EXISTS `parkingissue`;
USE `parkingissue`;

DELIMITER $$

CREATE FUNCTION bcrypt(password VARCHAR(255), cost INT)
RETURNS TEXT
DETERMINISTIC
BEGIN
    DECLARE salt TEXT;
    DECLARE hashed TEXT;
    SET salt = gensalt(cost); -- salt 생성
    SET hashed = crypt(password, salt); -- 비밀번호 암호화
    RETURN hashed;
END $$

DELIMITER ;

CREATE TABLE IF NOT EXISTS `user_info` (
    `userid` bigint(20) NOT NULL UNIQUE AUTO_INCREMENT,
    `nickname` varchar(255),
	`password` varchar(255),
    `naver_id` varchar(255),
    `kakao_id` varchar(255),
    PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `manager_info` (
    `managerid` bigint(20) NOT NULL UNIQUE AUTO_INCREMENT,
    `nickname` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`managerid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `parkingarea_info` (
    `pid` bigint(20) NOT NULL UNIQUE AUTO_INCREMENT,
    `park_id` varchar(255) NOT NULL UNIQUE,
    `park_nm` varchar(255) NOT NULL,
	`park_addr` varchar(255) NOT NULL,
	`park_la` float NOT NULL,
	`park_lo` float NOT NULL,
	`page_no` bigint(20) NOT NULL,
    PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `parkingarea_opertime` (
    `park_id` varchar(255) NOT NULL,
    `mon_opentime` varchar(255) NOT NULL,
    `mon_closetime` varchar(255) NOT NULL,
    `tue_opentime` varchar(255) NOT NULL,
    `tue_closetime` varchar(255) NOT NULL,
    `wed_opentime` varchar(255) NOT NULL,
    `wed_closetime` varchar(255) NOT NULL,
    `thu_opentime` varchar(255) NOT NULL,
    `thu_closetime` varchar(255) NOT NULL,
    `fri_opentime` varchar(255) NOT NULL,
    `fri_closetime` varchar(255) NOT NULL,
    `sat_opentime` varchar(255) NOT NULL,
    `sat_closetime` varchar(255) NOT NULL,
    `sun_opentime` varchar(255) NOT NULL,
    `sun_closetime` varchar(255) NOT NULL,
    `holi_opentime` varchar(255),
    `holi_closetime` varchar(255),
    PRIMARY KEY (`park_id`),
    FOREIGN KEY (`park_id`) REFERENCES `parkingarea_info` (`park_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `parkingarea_realtime` (
    `park_id` varchar(255) NOT NULL,
	`slot_total` int NOT NULL,
	`slot_available` int NOT NULL,
    PRIMARY KEY (`park_id`),
    FOREIGN KEY (`park_id`) REFERENCES `parkingarea_info` (`park_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `parkingarea_fee` (
    `park_id` varchar(255) NOT NULL,
    `free_time` int NOT NULL,
    `basic_fee` int NOT NULL,
    `adit_time` int NOT NULL,
    `adit_fee` int NOT NULL,
    `daily_fee` int NOT NULL,
    `monthly_fee` int NOT NULL,
    PRIMARY KEY (`park_id`),
    FOREIGN KEY (`park_id`) REFERENCES `parkingarea_info` (`park_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `fastival_info` (
    `fid` bigint(20) NOT NULL UNIQUE AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `eventstartdate` date NOT NULL,
    `eventenddate` date NOT NULL,
    `tel` varchar(255) NOT NULL,
    `firstimage` varchar(255) NOT NULL,
    `firstimage2` varchar(255) NOT NULL,
    `mapx` float NOT NULL,
    `mapy` float NOT NULL,
    PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `user_bookmarks` (
    `uid` bigint(20) NOT NULL,
    PRIMARY KEY (`uid`),
    FOREIGN KEY (`uid`) REFERENCES `user_info` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `manager_bookmarks` (
    `mid` bigint(20) NOT NULL,
    PRIMARY KEY (`mid`),
    FOREIGN KEY (`mid`) REFERENCES `manager_info` (`managerid`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `manager_festival` (
    `mid` bigint(20) NOT NULL,
    PRIMARY KEY (`mid`),
    FOREIGN KEY (`mid`) REFERENCES `manager_info` (`managerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE USER 'login'@'%' IDENTIFIED BY '$(LOGIN_PASSWORD)' WITH MAX_USER_CONNECTIONS 20;
GRANT SELECT ON parkingissue.user_info TO 'login'@'%';
GRANT SELECT ON parkingissue.manager_info TO 'login'@'%';
GRANT INSERT ON parkingissue.log_login TO 'login'@'%';

CREATE USER 'common_user'@'%'IDENTIFIED BY '$(USER_PASSWORD)' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT ON parkingissue.parkingarea_info TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_fee TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_opertime TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_realtime TO 'common_user'@'%';
GRANT SELECT, UPDATE ON parkingissue.user_info TO 'common_user'@'%';
GRANT INSERT ON parkingissue.log_cuser TO 'login'@'%';

CREATE USER 'manage_user'@'%'IDENTIFIED BY '$(USER_PASSWORD)' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT ON parkingissue.parkingarea_info TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_fee TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_opertime TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_realtime TO 'manage_user'@'%';
GRANT SELECT, UPDATE ON parkingissue.user_info TO 'manage_user'@'%';
GRANT INSERT ON parkingissue.log_muser TO 'login'@'%';

CREATE USER 'signup_user'@'%' IDENTIFIED BY '$(USER_PASSWORD)' WITH MAX_USER_CONNECTIONS 20;
GRANT INSERT, SELECT ON parkingissue.user_info TO 'signup_user'@'%';
GRANT INSERT ON parkingissue.log_csignup TO 'signup_user'@'%';
GRANT INSERT ON parkingissue.log_msignup TO 'signup_user'@'%';

CREATE USER 'exporter'@'%' IDENTIFIED BY '$(EXPORTER_PASSWORD)' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';

CREATE USER 'airflow_updater'@'%' IDENTIFIED BY '$(AIRFLOW_PASSWORD)' WITH MAX_USER_CONNECTIONS 1;
GRANT INSERT ON parkingissue.log_airflow TO 'airflow_updater'@'%';


FLUSH PRIVILEGES;
