CREATE DATABASE IF NOT EXISTS `bd_django_examples`;
USE `bd_django_examples`;

CREATE TABLE IF NOT EXISTS `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

INSERT INTO `client` (`id`, `name`, `mail`) VALUES
	(1, 'Client 1', 'contact@client1.com'),
	(2, 'Client 2', 'contact@client1.com');
