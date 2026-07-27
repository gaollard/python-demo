-- Forum schema for MySQL (compatible with SQLAlchemy create_all)
-- Prefer letting the app create tables on startup; use this for manual setup.

CREATE DATABASE IF NOT EXISTS forum DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE forum;

CREATE TABLE IF NOT EXISTS user_tab (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_username (username),
    KEY ix_user_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS post_tab (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    like_count INT NOT NULL DEFAULT 0,
    favorite_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    KEY ix_post_user_id (user_id),
    CONSTRAINT fk_post_user FOREIGN KEY (user_id) REFERENCES user_tab (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS post_like_tab (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_like_user_post (user_id, post_id),
    KEY ix_like_user_id (user_id),
    KEY ix_like_post_id (post_id),
    CONSTRAINT fk_like_user FOREIGN KEY (user_id) REFERENCES user_tab (id),
    CONSTRAINT fk_like_post FOREIGN KEY (post_id) REFERENCES post_tab (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS post_favorite_tab (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_favorite_user_post (user_id, post_id),
    KEY ix_favorite_user_id (user_id),
    KEY ix_favorite_post_id (post_id),
    CONSTRAINT fk_favorite_user FOREIGN KEY (user_id) REFERENCES user_tab (id),
    CONSTRAINT fk_favorite_post FOREIGN KEY (post_id) REFERENCES post_tab (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
