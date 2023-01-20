CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`metal_id`  INTERGER NOT NULL,
	`size_id` INTERGER NOT NULL,
	`style_id` INTERGER NOT NULL,
	FOREIGN KEY(`metal_id`) REFERENCES `Metals`(`id`),
	FOREIGN KEY(`size_id`) REFERENCES `Sizes`(`id`),
	FOREIGN KEY(`style_id`) REFERENCES `Styles`(`id`)
);

CREATE TABLE `Sizes` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`carets`  NUMERIC(3,2) NOT NULL,
	`price` NUMERIC(5,2) NOT NULL	
);

CREATE TABLE `Styles` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`style`  NVARCHAR(160) NOT NULL,
	`price` NUMERIC(5,2) NOT NULL	
);

INSERT INTO `Metals` VALUES (null, "Sterling Silver", 12.42);
INSERT INTO `Metals` VALUES (null, "14K Gold", 736.4);
INSERT INTO `Metals` VALUES (null, "24K Gold", 1258.9);
INSERT INTO `Metals` VALUES (null, "Platinum", 795.45);
INSERT INTO `Metals` VALUES (null, "Palladium", 1241);

INSERT INTO `Orders` VALUES (null, 1, 1, 1);
INSERT INTO `Orders` VALUES (null, 1, 2, 1);
INSERT INTO `Orders` VALUES (null, 2, 2, 1);
INSERT INTO `Orders` VALUES (null, 2, 2, 3);
INSERT INTO `Orders` VALUES (null, 5, 2, 1);
INSERT INTO `Orders` VALUES (null, 4, 1, 2);

INSERT INTO `Styles` VALUES (null, "Classic", 500.00);
INSERT INTO `Styles` VALUES (null, "Modern", 710.00);
INSERT INTO `Styles` VALUES (null, "Vintage", 965.00);

INSERT INTO `Sizes` VALUES (null, 0.5, 405.00);
INSERT INTO `Sizes` VALUES (null, 0.75, 782.00);
INSERT INTO `Sizes` VALUES (null, 1, 1470.00);
INSERT INTO `Sizes` VALUES (null, 1.5, 1997.00);
INSERT INTO `Sizes` VALUES (null, 2, 3638.00);
