-- CREATE DATABASE IF NOT EXISTS monitoring;

CREATE TABLE IF NOT EXISTS disk (
    total_disk REAL,
    total_used REAL,
    total_free REAL,
    percent REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);