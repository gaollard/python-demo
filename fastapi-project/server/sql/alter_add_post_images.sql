-- Add images column for existing databases (MySQL 8+)
ALTER TABLE post_tab
    ADD COLUMN images JSON NOT NULL DEFAULT (JSON_ARRAY()) AFTER content;
