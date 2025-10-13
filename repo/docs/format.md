# 数据传输格式

## 上传格式

数据类型为 JSON，格式如下：

### URL

```
127.0.0.1/api/send?data=[gamedata]
```

### gamedata

```json
gamedata = {
    "timestamp":    1760354236,         // 时间戳
    "mod_version":  {                   // 使用的模组版本
        "ccb_version":          "1200",
        "ccb_map_version":      "1100",
        "ccb_mph_version":      "1100",
        "ccb_exp_version":      "1100",
        "[Other Mod]_version":  "1234"
    },
    "map_type": "RICH_HIGHLANDS",       // 地图类型
    "player_num": 8,                    // 玩家数量
    "total_turns": 89,                  // 游戏回合数
    "player_leader_civ":    {           // 玩家 ID、分队、使用的领袖和文明
        "[Steam ID 1]": {
            "team":                 1,
            "leader_type":          "LEADER_QIN",
            "civilization_type":    "CIVILIZATION_CHINA"
        },
        "[Steam ID 2]": {
            "team":                 2,
            "leader_type":          "LEADER_QIN_ALT",
            "civilization_type":    "CIVILIZATION_CHINA"
        }
    },
    "winner_team":  1                   // 获胜队伍
}
```