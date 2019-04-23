-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: tickets
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text,
  `subject` text,
  `body` text,
  `status` text,
  `date` text,
  `response` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (2,'max','subject','this%20is%20the%20body','Closed',NULL,'hi ticket number 3'),(3,'max','subject','this%20is%20the%20body','in-progress',NULL,'this%20is%20a%20test%20responsesssss'),(4,'max','subject','this%20is%20a%20great%20answer','in-progress',NULL,'this%20is%20a%20great%20answer'),(5,'max','subject','this%20is%20the%20body','Closed','2019-03-31 07:42:20',NULL),(6,'max','subject','this%20is%20the%20body','Closed','1970-01-01 00:00:04',NULL),(7,'max','subject','this%20is%20the%20body','bye%20bye','1969-12-31 23:59:56',NULL),(8,'max','subject','this%20is%20the%20body','Closed','2019-03-31 07:43:18','this%20is%20a%20great%20answer'),(9,'max','subject','this%20is%20the%20body','Closed','2019-03-31 08:20:41',NULL),(10,'warren','subject','this%20is%20the%20body','open','2019-03-31 08:20:49',NULL),(11,'william','subject','this%20is%20the%20body','Closed','2019-04-03 15:37:12','this%20is%20a%20great%20answer'),(12,'william','testing','hello%20my%20friend','open','2019-04-03 15:37:42',NULL),(13,'max','testsubject z','test body for the send ticket route z','open','2019-04-07 13:45:32',NULL),(14,'max','testsubject z','test body for the send ticket route z','open','2019-04-07 13:53:53',NULL),(15,'max','testsubject z','test body for the send ticket route z','open','2019-04-07 13:57:33',NULL),(16,'max','%0A','%0A','open','2019-04-07 21:07:32',NULL),(17,'max','text+subject%0A','text+body%0A','open','2019-04-07 21:08:39',NULL),(18,'max','testsubjectssss','test%20body%20for%20the%20send%20ticket%20routessss','open','2019-04-19 13:47:02',NULL),(19,'max','hi%0A','hiii%0A','open','2019-04-19 14:03:01',NULL);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `firstname` text,
  `lastname` text,
  `token` text,
  `isAdmin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'hadi','1234',NULL,NULL,'639e5ccf7181b6477e7dbb62e3a44daa',0),(7,'maxine','1234','','','5ff48b4047c44e97f578199ca6cd2865',0),(8,'chloeprice','1234','','','5954fb4064ebccaeefd0420f11ab2027',0),(9,'max','1234','','','cffe8ab779cf5e0873087a554b02c88f',1),(10,'warren','1234','','','673420f64a5afb40bc033bb958dd336c',0),(11,'william','1234','william','price','e1b7d93c6a72abba9f1cb6c323815737',0),(12,'joyce','1234','','','',0),(13,'clay','1234','','',NULL,0),(14,'victoria','1234','victoria','',NULL,0),(15,'frank','1234','','',NULL,0),(16,'franks','1234','','','8a0c903d32559d767a8120621d4b94f2',0),(17,'maxinee','1234','','',NULL,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-23 15:50:29
