-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        11.8.2-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- mydb 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `mydb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `mydb`;

-- 테이블 mydb.auth_group 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_group:~0 rows (대략적) 내보내기

-- 테이블 mydb.auth_group_permissions 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_group_permissions:~0 rows (대략적) 내보내기

-- 테이블 mydb.auth_permission 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_permission:~32 rows (대략적) 내보내기
REPLACE INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add contact', 7, 'add_contact'),
	(26, 'Can change contact', 7, 'change_contact'),
	(27, 'Can delete contact', 7, 'delete_contact'),
	(28, 'Can view contact', 7, 'view_contact'),
	(29, 'Can add psy', 8, 'add_psy'),
	(30, 'Can change psy', 8, 'change_psy'),
	(31, 'Can delete psy', 8, 'delete_psy'),
	(32, 'Can view psy', 8, 'view_psy');

-- 테이블 mydb.auth_user 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_user:~0 rows (대략적) 내보내기

-- 테이블 mydb.auth_user_groups 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_user_groups:~0 rows (대략적) 내보내기

-- 테이블 mydb.auth_user_user_permissions 구조 내보내기
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.auth_user_user_permissions:~0 rows (대략적) 내보내기

-- 테이블 mydb.django_admin_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.django_admin_log:~0 rows (대략적) 내보내기

-- 테이블 mydb.django_content_type 구조 내보내기
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.django_content_type:~8 rows (대략적) 내보내기
REPLACE INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(3, 'auth', 'group'),
	(2, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(7, 'myapp', 'contact'),
	(8, 'myapp', 'psy'),
	(6, 'sessions', 'session');

-- 테이블 mydb.django_migrations 구조 내보내기
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.django_migrations:~20 rows (대략적) 내보내기
REPLACE INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2025-07-22 08:07:57.281050'),
	(2, 'auth', '0001_initial', '2025-07-22 08:07:57.811851'),
	(3, 'admin', '0001_initial', '2025-07-22 08:07:57.915855'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2025-07-22 08:07:57.920863'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-22 08:07:57.927315'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2025-07-22 08:07:58.015064'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2025-07-22 08:07:58.063672'),
	(8, 'auth', '0003_alter_user_email_max_length', '2025-07-22 08:07:58.098333'),
	(9, 'auth', '0004_alter_user_username_opts', '2025-07-22 08:07:58.103318'),
	(10, 'auth', '0005_alter_user_last_login_null', '2025-07-22 08:07:58.149140'),
	(11, 'auth', '0006_require_contenttypes_0002', '2025-07-22 08:07:58.152140'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-22 08:07:58.160151'),
	(13, 'auth', '0008_alter_user_username_max_length', '2025-07-22 08:07:58.197008'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-22 08:07:58.231671'),
	(15, 'auth', '0010_alter_group_name_max_length', '2025-07-22 08:07:58.268603'),
	(16, 'auth', '0011_update_proxy_permissions', '2025-07-22 08:07:58.284587'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-22 08:07:58.339108'),
	(18, 'sessions', '0001_initial', '2025-07-22 08:07:58.391234'),
	(19, 'myapp', '0001_initial', '2025-07-22 08:12:32.292035'),
	(20, 'myapp', '0002_psy_delete_contact', '2025-07-23 01:35:55.307695');

-- 테이블 mydb.django_session 구조 내보내기
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.django_session:~1 rows (대략적) 내보내기
REPLACE INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('s5mqugaed170vbit8t08z9y7dg5yp3mp', 'eyJ1c2VyIjoic2V5dW4ifQ:1ueqtr:IWLFfuvvpuNUMoLGzAE1c2DPPEUdLAvSpPKdngkPryo', '2025-08-07 08:01:59.156468');

-- 테이블 mydb.notes 구조 내보내기
CREATE TABLE IF NOT EXISTS `notes` (
  `note_id` uuid NOT NULL,
  `title` varchar(50) NOT NULL,
  `content` text DEFAULT NULL,
  `last_modified` datetime NOT NULL,
  `user_pid` uuid NOT NULL,
  PRIMARY KEY (`note_id`),
  KEY `FK_notes_users` (`user_pid`),
  CONSTRAINT `FK_notes_users` FOREIGN KEY (`user_pid`) REFERENCES `users` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.notes:~1 rows (대략적) 내보내기
REPLACE INTO `notes` (`note_id`, `title`, `content`, `last_modified`, `user_pid`) VALUES
	('50dd7ff7-686b-11f0-a836-d843ae370a3f', '테스트 제목', '테스트 내용', '2025-07-24 17:50:26', 'fa3da424-c9f3-496a-a34d-90b0fdf5ce6f');

-- 테이블 mydb.psy 구조 내보내기
CREATE TABLE IF NOT EXISTS `psy` (
  `name` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.psy:~1 rows (대략적) 내보내기
REPLACE INTO `psy` (`name`, `number`) VALUES
	(2, 3);

-- 테이블 mydb.users 구조 내보내기
CREATE TABLE IF NOT EXISTS `users` (
  `pid` uuid NOT NULL,
  `username` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(20) NOT NULL,
  `nickname` varchar(20) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 테이블 데이터 mydb.users:~1 rows (대략적) 내보내기
REPLACE INTO `users` (`pid`, `username`, `password`, `nickname`) VALUES
	('fa3da424-c9f3-496a-a34d-90b0fdf5ce6f', 'seyun', '1234', '세윤');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
