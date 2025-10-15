DROP TABLE IF EXISTS Games;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS GamePlayers;

CREATE TABLE Games (
    game_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    timestamp BIGINT NOT NULL,
    game_seed BIGINT NOT NULL,
    map_seed BIGINT NOT NULL,
    map_type VARCHAR(100) NOT NULL,
    player_num INT NOT NULL,
    total_turns INT NOT NULL,
    winner_team INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Players (
    player_id VARCHAR(20) PRIMARY KEY, -- 17位Steam ID作为主键
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE GamePlayers (
    game_id BIGINT NOT NULL,
    player_id VARCHAR(20) NOT NULL,
    player_code VARCHAR(10) NOT NULL, -- '00', '01', etc.
    team INT NOT NULL,
    leader_type VARCHAR(100) NOT NULL,
    civilization_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id, player_id), -- 复合主键
    FOREIGN KEY (game_id) REFERENCES Games(game_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES Players(player_id) ON DELETE CASCADE
);

