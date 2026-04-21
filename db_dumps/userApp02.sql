-- MySQL dump 10.13  Distrib 8.0.27, for macos11 (x86_64)
--
-- Host: localhost    Database: noveleshelf_noveleshelf
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `userApp_authorrequest`
--

DROP TABLE IF EXISTS `userApp_authorrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_authorrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `request_type` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `bio` longtext,
  `genre_interest` varchar(100) DEFAULT NULL,
  `writing_sample_link` varchar(200) DEFAULT NULL,
  `admin_notes` longtext,
  `reader_notes` longtext,
  `contact_attempted` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userApp_authorrequest_user_id_b905edd5_fk_userApp_user_id` (`user_id`),
  CONSTRAINT `userApp_authorrequest_user_id_b905edd5_fk_userApp_user_id` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userApp_emailverificationtoken`
--

DROP TABLE IF EXISTS `userApp_emailverificationtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_emailverificationtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(64) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `userApp_emailverific_user_id_2f1a61a7_fk_userApp_u` (`user_id`),
  CONSTRAINT `userApp_emailverific_user_id_2f1a61a7_fk_userApp_u` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userApp_freeauthorprofile`
--

DROP TABLE IF EXISTS `userApp_freeauthorprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_freeauthorprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `author_username` varchar(50) DEFAULT NULL,
  `pen_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `show_real_name` tinyint(1) NOT NULL,
  `is_publicly_visible` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `bio` longtext,
  `avatar_url` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `author_username` (`author_username`),
  CONSTRAINT `userApp_freeauthorprofile_user_id_95617a8f_fk_userApp_user_id` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userApp_passwordresettoken`
--

DROP TABLE IF EXISTS `userApp_passwordresettoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userApp_passwordresettoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(64) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `userApp_passwordresettoken_user_id_67cdc07b_fk_userApp_user_id` (`user_id`),
  CONSTRAINT `userApp_passwordresettoken_user_id_67cdc07b_fk_userApp_user_id` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21 14:01:57
