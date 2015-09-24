PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE `work` (
`id` INTEGER PRIMARY KEY,
`userid` INTEGER,
`input` TEXT NOT NULL,
`output` BLOB,                   -- PDF FILE
`starttime` TEXT NOT NULL,    -- UNIX TIME, float
`stoptime` TEXT,
`status` TEXT NOT NULL,          -- 'I', 'R', 'E', 'X', 'S'
`log` TEXT);
COMMIT;
