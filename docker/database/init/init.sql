CREATE DATABASE IF NOT EXISTS `parkingissue`;
USE `parkingissue`;

CREATE TABLE IF NOT EXISTS `userinfo` (
    `userid` bigint(20) NOT NULL AUTO_INCREMENT,
    `nickname` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
    PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `managerinfo` (
    `managerid` bigint(20) NOT NULL AUTO_INCREMENT,
    `nickname` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    PRIMARY KEY (`managerid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `parkingarea_info` (
    `pid` bigint(20) NOT NULL AUTO_INCREMENT,
    `park_id` varchar(255) NOT NULL,
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
    `fid` bigint(20) NOT NULL,
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

CREATE TABLE IF NOT EXISTS `log_login` (
    `index` bigint(20)
    `ip` varchar(20),
    `uid` bigint(20),
    `result` boolean,
    `time` date,
    PRIMARY KEY (`index`),
    FOREIGN KEY (`uid`) REFERENCES `user_info` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `log_csignup` (
    `index` bigint(20)
    `ip` varchar(20),
    `uid` bigint(20),
    `type` int,
    `time` date,
    PRIMARY KEY (`index`),
    FOREIGN KEY (`uid`) REFERENCES `user_info` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `log_msignup` (
    `index` bigint(20)
    `ip` varchar(20),
    `mid` bigint(20),
    `time` date,
    PRIMARY KEY (`index`),
    FOREIGN KEY (`mid`) REFERENCES `manager_info` (`managerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `log_cuser` (
    `index` bigint(20)
    `ip` varchar(20),
    `uid` bigint(20),
    `request` varchar(255)
    `time` date,
    PRIMARY KEY (`index`),
    FOREIGN KEY (`uid`) REFERENCES `user_info` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `log_muser` (
    `index` bigint(20)
    `ip` varchar(20),
    `mid` bigint(20),
    `result` boolean,
    `time` date,
    PRIMARY KEY (`index`),
    FOREIGN KEY (`mid`) REFERENCES `manager_info` (`managerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `log_airflow` (
    `index` bigint(20), AUTO_INCREMENT
    `time` date,
    `request` varchar(255),
    `result` boolean,
    PRIMARY KEY ()`index`
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE USER 'login'@'%' IDENTIFIED BY 'login' WITH MAX_USER_CONNECTIONS 20;
GRANT SELECT ON parkingissue.userinfo TO 'login'@'%';
GRANT SELECT ON parkingissue.managerinfo TO 'login'@'%';
GRANT INSERT ON parkingissue.log_login TO 'login'@'%';

CREATE USER 'common_user'@'%'IDENTIFIED BY 'login' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT ON parkingissue.parkingarea_info TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_fee TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_opertime TO 'common_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_realtime TO 'common_user'@'%';
GRANT SELECT, UPDATE ON parkingissue.userinfo TO 'common_user'@'%';
GRANT INSERT ON parkingissue.log_cuser TO 'login'@'%';

CREATE USER 'manage_user'@'%'IDENTIFIED BY 'login' WITH MAX_USER_CONNECTIONS 1000;
GRANT SELECT ON parkingissue.parkingarea_info TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_fee TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_opertime TO 'manage_user'@'%';
GRANT SELECT ON parkingissue.parkingarea_realtime TO 'manage_user'@'%';
GRANT SELECT, UPDATE ON parkingissue.userinfo TO 'manage_user'@'%';
GRANT INSERT ON parkingissue.log_muser TO 'login'@'%';

CREATE USER 'signup_user'@'%' IDENTIFIED BY 'signup' WITH MAX_USER_CONNECTIONS 20;
GRANT INSERT, SELECT ON parkingissue.userinfo TO 'signup_user'@'%';
GRANT INSERT ON parkingissue.log_csignup TO 'signup_user'@'%';
GRANT INSERT ON parkingissue.log_msignup TO 'signup_user'@'%';

CREATE USER 'exporter'@'%' IDENTIFIED BY 'five2024$' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';

CREATE USER 'airflow_updater'@'%' IDENTIFIED BY 'five2024$' WITH MAX_USER_CONNECTIONS 1;
GRANT INSERT ON parkingissue.log_airflow BY 'airflow_updater'@'%';


FLUSH PRIVILEGES;