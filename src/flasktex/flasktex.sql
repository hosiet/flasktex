PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
    DROP TABLE IF EXISTS `metadata`;
    CREATE TABLE `metadata` (
        `api_level` INTEGER NOT NULL,
        `comment` TEXT);
    DROP TABLE IF EXISTS `work`;
    CREATE TABLE `work` (
        `id` INTEGER PRIMARY KEY,
        `retrieve_id` TEXT NOT NULL,
        `targz_data` BLOB NOT NULL,
        `entryfile` TEXT NOT NULL,
        `output` BLOB,
        `start_time` TEXT NOT NULL, -- OUTPUT OF Py: time.time()
        `stop_time` TEXT,
        `status` TEXT NOT NULL, -- 'INIT', 'RUNNING', 'FAILURE', 'SUCCESS', 'DELETED'
        `log` TEXT);
COMMIT;
