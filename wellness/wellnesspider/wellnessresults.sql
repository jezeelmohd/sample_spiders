-- phpMyAdmin SQL Dump
-- version 4.0.0
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 14, 2013 at 07:23 PM
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
-- Table structure for table `wellnessresults`
--

CREATE TABLE IF NOT EXISTS `wellnessresults` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `eid` int(10) NOT NULL DEFAULT '0',
  `URL` varchar(100) CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `author` varchar(100) CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `review_date` varchar(100) CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `review_text` text CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `rating` varchar(100) CHARACTER SET utf32 COLLATE utf32_unicode_ci NOT NULL,
  `LastCrawl` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sentiment` tinyint(4) NOT NULL,
  `sentiment_update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
