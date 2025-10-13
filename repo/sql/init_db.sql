DROP TABLE IF EXISTS Games;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS GamePlayers;

CREATE TABLE IF NOT EXISTS Games (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    game_time_stamp INTEGER,
    ccb_version     TEXT,
    ccb_map_version TEXT,
    ccb_mph_version TEXT,
    ccb_exp_version TEXT,
    map_type        TEXT,
    player_num      INTEGER,
    total_turns     INTEGER,
    winner_team     INTEGER
);

CREATE TABLE IF NOT EXISTS Players (
    id              TEXT PRIMARY KEY,
    total_game_num  INT DEFAULT 0,
    won_game_num    INT DEFAULT 0,
    win_rate        REAL DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS GamePlayers (
    game_id             INTEGER NOT NULL,
    player_id           TEXT NOT NULL,
    team                INTEGER,
    is_winner           BOOLEAN,
    leader_type         TEXT,
    civilization_type   TEXT,
    PRIMARY KEY (game_id, player_id),
    FOREIGN KEY (game_id) REFERENCES Games(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES Players(id) ON DELETE CASCADE
);

