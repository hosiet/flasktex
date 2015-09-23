PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE `work` (
id INTEGER PRIMARY KEY,
uid INTEGER,
input TEXT NOT NULL,
output BLOB,                   -- PDF FILE
starttime INTEGER NOT NULL,    -- UNIX TIME
stoptime INTEGER,
status TEXT NOT NULL,          -- 'I', 'R', 'E', 'X', 'F'
extra TEXT);
COMMIT;
