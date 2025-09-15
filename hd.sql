-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 15, 2025 at 04:21 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hd`
--

-- --------------------------------------------------------

--
-- Table structure for table `count_polygon`
--

CREATE TABLE `count_polygon` (
  `id_count` int(11) NOT NULL,
  `id_polygon` int(11) NOT NULL,
  `count_in` int(11) NOT NULL,
  `count_out` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `count_polygon`
--

INSERT INTO `count_polygon` (`id_count`, `id_polygon`, `count_in`, `count_out`) VALUES
(2, 2, 0, 0),
(11, 14, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `detected_polygon`
--

CREATE TABLE `detected_polygon` (
  `id_detected` int(11) NOT NULL,
  `id_polygon` int(11) NOT NULL,
  `uuid_object` varchar(50) NOT NULL,
  `time_in` datetime NOT NULL,
  `time_out` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `polygon`
--

CREATE TABLE `polygon` (
  `id_polygon` int(11) NOT NULL,
  `name_polygon` varchar(50) NOT NULL,
  `pts1_x` int(11) NOT NULL,
  `pts1_y` int(11) NOT NULL,
  `pts2_x` int(11) NOT NULL,
  `pts2_y` int(11) NOT NULL,
  `pts3_x` int(11) NOT NULL,
  `pts3_y` int(11) NOT NULL,
  `pts4_x` int(11) NOT NULL,
  `pts4_y` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `polygon`
--

INSERT INTO `polygon` (`id_polygon`, `name_polygon`, `pts1_x`, `pts1_y`, `pts2_x`, `pts2_y`, `pts3_x`, `pts3_y`, `pts4_x`, `pts4_y`) VALUES
(2, 'area2', 220, 150, 320, 170, 250, 250, 120, 230),
(14, 'areatest', 290, 260, 380, 290, 430, 200, 340, 180);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `count_polygon`
--
ALTER TABLE `count_polygon`
  ADD PRIMARY KEY (`id_count`),
  ADD KEY `count_polygon` (`id_polygon`);

--
-- Indexes for table `detected_polygon`
--
ALTER TABLE `detected_polygon`
  ADD PRIMARY KEY (`id_detected`),
  ADD KEY `detected_polygon` (`id_polygon`);

--
-- Indexes for table `polygon`
--
ALTER TABLE `polygon`
  ADD PRIMARY KEY (`id_polygon`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `count_polygon`
--
ALTER TABLE `count_polygon`
  MODIFY `id_count` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `detected_polygon`
--
ALTER TABLE `detected_polygon`
  MODIFY `id_detected` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `polygon`
--
ALTER TABLE `polygon`
  MODIFY `id_polygon` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `count_polygon`
--
ALTER TABLE `count_polygon`
  ADD CONSTRAINT `count_polygon` FOREIGN KEY (`id_polygon`) REFERENCES `polygon` (`id_polygon`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `detected_polygon`
--
ALTER TABLE `detected_polygon`
  ADD CONSTRAINT `detected_polygon` FOREIGN KEY (`id_polygon`) REFERENCES `polygon` (`id_polygon`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
