CREATE TABLE IF NOT EXISTS `quotes` (
  `id` bigint(20) NOT NULL,
  `nick` varchar(20) NOT NULL DEFAULT '',
  `host` varchar(100) NOT NULL DEFAULT '',
  `quote` text NOT NULL,
  `channel` varchar(50) NOT NULL DEFAULT '',
  `timestamp` bigint(20) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
