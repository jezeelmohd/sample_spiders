-- phpMyAdmin SQL Dump
-- version 4.0.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 19, 2013 at 12:47 PM
-- Server version: 5.5.31-0ubuntu0.12.10.1
-- PHP Version: 5.4.6-1ubuntu1.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `cubator`
--

-- --------------------------------------------------------

--
-- Table structure for table `bingresults`
--

CREATE TABLE IF NOT EXISTS `bingresults` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `eid` int(11) DEFAULT NULL,
  `URL` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Title` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Summary` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Description` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Rank` tinyint(5) DEFAULT NULL,
  `Keyword` text COLLATE utf8_unicode_ci,
  `Lastcrawl` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Source` text COLLATE utf8_unicode_ci,
  `Destinationtext` text COLLATE utf8_unicode_ci,
  `text_rating` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sentiment` tinyint(4) DEFAULT NULL,
  `sentiment_update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `URL` (`URL`),
  KEY `eid` (`eid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
