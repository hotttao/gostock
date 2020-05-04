CREATE DATABASE stock;
USE stock;

CREATE TABLE `event` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event` VARCHAR(255) NOT NULL,
  `sub_event` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL
);

CREATE TABLE `event_occur` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event_id` INTEGER NOT NULL,
  `date` DATE NOT NULL
);

CREATE INDEX `idx_event_occur__event_id` ON `event_occur` (`event_id`);

ALTER TABLE `event_occur` ADD CONSTRAINT `fk_event_occur__event_id` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE;

CREATE TABLE `event_influence` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `event_occur_id` INTEGER NOT NULL,
  `level` INTEGER NOT NULL
);

CREATE INDEX `idx_event_influence__event_occur_id` ON `event_influence` (`event_occur_id`);

ALTER TABLE `event_influence` ADD CONSTRAINT `fk_event_influence__event_occur_id` FOREIGN KEY (`event_occur_id`) REFERENCES `event_occur` (`id`) ON DELETE CASCADE;

CREATE TABLE `industry` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `industry` VARCHAR(255) NOT NULL,
  `sub_industry` VARCHAR(255) NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `event_influence` INTEGER
);

CREATE INDEX `idx_industry__event_influence` ON `industry` (`event_influence`);

ALTER TABLE `industry` ADD CONSTRAINT `fk_industry__event_influence` FOREIGN KEY (`event_influence`) REFERENCES `event_influence` (`id`) ON DELETE SET NULL;

CREATE TABLE `index_champion_index` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `industry_id` INTEGER NOT NULL,
  `value` DOUBLE NOT NULL
);

CREATE INDEX `idx_index_champion_index__industry_id` ON `index_champion_index` (`industry_id`);

ALTER TABLE `index_champion_index` ADD CONSTRAINT `fk_index_champion_index__industry_id` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE;

CREATE TABLE `industry_index` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `industry_id` INTEGER NOT NULL,
  `value` DOUBLE NOT NULL
);

CREATE INDEX `idx_industry_index__industry_id` ON `industry_index` (`industry_id`);

ALTER TABLE `industry_index` ADD CONSTRAINT `fk_industry_index__industry_id` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE;

CREATE TABLE `stocks` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `is_champion` TINYINT NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `industry_id` INTEGER NOT NULL
);

CREATE INDEX `idx_stocks__industry_id` ON `stocks` (`industry_id`);

ALTER TABLE `stocks` ADD CONSTRAINT `fk_stocks__industry_id` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE;

CREATE TABLE `transaction` (
  `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `stock_id` INTEGER NOT NULL,
  `date` DATE NOT NULL,
  `price` DOUBLE NOT NULL
);

CREATE INDEX `idx_transaction__stock_id` ON `transaction` (`stock_id`);

ALTER TABLE `transaction` ADD CONSTRAINT `fk_transaction__stock_id` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`id`) ON DELETE CASCADE