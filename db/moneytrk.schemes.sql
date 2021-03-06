BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category_name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "transactions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"category"	TEXT NOT NULL,
	"amount"	NUMERIC NOT NULL,
	"description"	TEXT,
	PRIMARY KEY("id")
);
COMMIT;
