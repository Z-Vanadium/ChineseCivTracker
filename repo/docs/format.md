# 数据传输格式

## 上传格式

数据类型为 JSON，格式如下：

### URL

```
http://60.205.246.25:80/api/send?data=[gamedata]
```

### gamedata

```json
data = {
    "timestamp":    1760354236,         // 时间戳
    "game_seed":    638722508,
    "map_seed":     638722509,          // 种子
    "mod_version":  {                   // 使用的模组版本
        "ccb_version":          "1200",
        "ccb_map_version":      "1100",
        "ccb_mph_version":      "1100",
        "ccb_exp_version":      "1100",
        "[Other Mod]_version":  "1234"
    },
    "map_type": "RICH_HIGHLANDS",       // 地图类型
    "player_num": 8,                    // 真人玩家数量
    "total_turns": 89,                  // 游戏回合数
    "player_leader_civ":    {           // 玩家 ID、分队、使用的领袖和文明
        "00": {                         // 玩家楼层，00 为一楼
            "steam_id": "[17 位数字]",
            "team":                 1,
            "leader_type":          "LEADER_QIN",
            "civilization_type":    "CIVILIZATION_CHINA"
        },
        "01": {
            "steam_id": "[17 位数字]",
            "team":                 2,
            "leader_type":          "LEADER_QIN_ALT",
            "civilization_type":    "CIVILIZATION_CHINA"
        }
        // ...
    },
    "winner_team":  1,                  // 获胜队伍
    "game_summary": {                   // 游戏数据统计
        "10": {                         // 回合数
            "00": {                         // 玩家楼层，00 为一楼
                "s": 1.0,                   // Science 科技值
                "c": 2.0,                   // Culture 文化值
                "g": 30,                    // Gold 现金
                "f": 4.0                    // Faith 回合信仰
            }
            // ...
        }
        // ...
    }
}
```

## 数据库

### DDL

```sql
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
```