BEGIN TRANSACTION;
CREATE TABLE "people" (
	`Id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`gender`	INTEGER,
	PRIMARY KEY(`Id`)
);
INSERT INTO `people` VALUES (1,'Felipe M','M');
INSERT INTO `people` VALUES (2,'Elder Bednar',NULL);
INSERT INTO `people` VALUES (3,' Zach',NULL);
COMMIT;
