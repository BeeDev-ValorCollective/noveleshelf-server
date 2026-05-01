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
-- Table structure for table `notificationApp_notification`
--

DROP TABLE IF EXISTS `notificationApp_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `notification_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notificationApp_notification_user_id_6a819918_fk_userApp_user_id` (`user_id`),
  KEY `notificationApp_noti_notification_type_id_6cb22bef_fk_notificat` (`notification_type_id`),
  CONSTRAINT `notificationApp_noti_notification_type_id_6cb22bef_fk_notificat` FOREIGN KEY (`notification_type_id`) REFERENCES `notificationApp_notificationtype` (`id`),
  CONSTRAINT `notificationApp_notification_user_id_6a819918_fk_userApp_user_id` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notificationApp_notificationpermission`
--

DROP TABLE IF EXISTS `notificationApp_notificationpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_notificationpermission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_allowed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `granted_by_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `notification_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notificationApp_notifica_user_id_notification_typ_53d8a4b3_uniq` (`user_id`,`notification_type_id`),
  KEY `notificationApp_noti_granted_by_id_bb05b8bf_fk_userApp_u` (`granted_by_id`),
  KEY `notificationApp_noti_notification_type_id_40d87a78_fk_notificat` (`notification_type_id`),
  CONSTRAINT `notificationApp_noti_granted_by_id_bb05b8bf_fk_userApp_u` FOREIGN KEY (`granted_by_id`) REFERENCES `userApp_user` (`id`),
  CONSTRAINT `notificationApp_noti_notification_type_id_40d87a78_fk_notificat` FOREIGN KEY (`notification_type_id`) REFERENCES `notificationApp_notificationtype` (`id`),
  CONSTRAINT `notificationApp_noti_user_id_2e6a4255_fk_userApp_u` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notificationApp_notificationpreference`
--

DROP TABLE IF EXISTS `notificationApp_notificationpreference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_notificationpreference` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_enabled` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `notification_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notificationApp_notifica_user_id_notification_typ_0e763cd3_uniq` (`user_id`,`notification_type_id`),
  KEY `notificationApp_noti_notification_type_id_ae262908_fk_notificat` (`notification_type_id`),
  CONSTRAINT `notificationApp_noti_notification_type_id_ae262908_fk_notificat` FOREIGN KEY (`notification_type_id`) REFERENCES `notificationApp_notificationtype` (`id`),
  CONSTRAINT `notificationApp_noti_user_id_3e954cb2_fk_userApp_u` FOREIGN KEY (`user_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notificationApp_notificationtype`
--

DROP TABLE IF EXISTS `notificationApp_notificationtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_notificationtype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) NOT NULL,
  `label` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `recipient_type` varchar(10) NOT NULL,
  `sends_to_user` tinyint(1) NOT NULL,
  `sends_to_admins` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notificationApp_systemnotificationemail`
--

DROP TABLE IF EXISTS `notificationApp_systemnotificationemail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_systemnotificationemail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `label` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `notificationApp_syst_created_by_id_d6d120de_fk_userApp_u` (`created_by_id`),
  CONSTRAINT `notificationApp_syst_created_by_id_d6d120de_fk_userApp_u` FOREIGN KEY (`created_by_id`) REFERENCES `userApp_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notificationApp_systemnotificationemail_notification_types`
--

DROP TABLE IF EXISTS `notificationApp_systemnotificationemail_notification_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificationApp_systemnotificationemail_notification_types` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `systemnotificationemail_id` bigint NOT NULL,
  `notificationtype_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notificationApp_systemno_systemnotificationemail__d4e54b57_uniq` (`systemnotificationemail_id`,`notificationtype_id`),
  KEY `notificationApp_syst_notificationtype_id_d34e90ad_fk_notificat` (`notificationtype_id`),
  CONSTRAINT `notificationApp_syst_notificationtype_id_d34e90ad_fk_notificat` FOREIGN KEY (`notificationtype_id`) REFERENCES `notificationApp_notificationtype` (`id`),
  CONSTRAINT `notificationApp_syst_systemnotificationem_1a37a318_fk_notificat` FOREIGN KEY (`systemnotificationemail_id`) REFERENCES `notificationApp_systemnotificationemail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-01 16:17:13
