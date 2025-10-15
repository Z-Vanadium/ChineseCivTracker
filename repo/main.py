from flask import Flask, g, request, jsonify
import sqlite3
import json
import logging
from datetime import datetime

DEBUG = True
HOST = '60.205.246.25'
PORT = 80

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ChineseCivTracker')

app = Flask(__name__)
app.config['DATABASE'] = '../__db__/civ_tracker.db'

def _Debug(*values: object):
    print('[DEBUG]', *values)
    
@app.route('/api/send', methods=['GET']) # type: ignore
def route_api_send():
    try:
        game_data_str = request.args.get('data')
        if not game_data_str:
            return jsonify({"status": "error", "message": "缺少数据参数"}), 400
        
        game_data = json.loads(game_data_str)
        # _Debug(f'Get gamedata: {game_data_str}')
        
        game_id = save_game_data(game_data)
        
        return jsonify({
            "status": "success", 
            "message": "数据接收成功",
            "game_id": game_id
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
        return jsonify({"status": "error", "message": "数据格式错误"}), 400
    
def save_game_data(game_data: dict[str, any]) -> int: # type: ignore
    '''
    save game data into database
    '''
    db = get_db()
    
    try:
        game_data = validate_game_data(game_data)
        if not game_data:
            return 0
        timestamp = int(game_data.get('timestamp', int(datetime.now().timestamp())))
        if timestamp:
            # check if time stamp in 10 sec is existing
            # existing_game = find_duplicate_game_by_timestamp(db, timestamp, tolerance_seconds=10)
            existing_game = False
            if existing_game:
                _Debug(f"Exisiting time stamp in 10 sec in game with id: {existing_game['id']}")
                return -1  # 返回特殊值表示重复数据

        player_leader_civ: dict[str, any] = game_data.get('player_leader_civ', {}) # type: ignore
        mod_version: dict[str, any] = game_data.get('mod_version', {}) # pyright: ignore[reportGeneralTypeIssues]
        winner_team = game_data.get('winner_team')
        
        # game data
        cursor = db.execute('''
            INSERT INTO Games (time_stamp, map_type, player_num, total_turns, winner_team, game_seed, map_seed) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
                timestamp,
                game_data.get('map_type'),
                game_data.get('player_num'),
                game_data.get('total_turns'),
                game_data.get('winner_team'),
                game_data.get('game_seed'),
                game_data.get('map_seed')
            )
        )
        game_id = cursor.lastrowid
        
        # player data and gameplayer data
        for player_code, player_info in player_leader_civ.items():
            steam_id = player_info.get('steam_id')
            if steam_id is None:
                continue
            is_winner: bool = (player_info.get('team') == winner_team)
            # player data
            # if is_winner:
            #     # is winner
            #     db.execute('''
            #         INSERT INTO Players (id, total_game_num, won_game_num, win_rate)
            #         VALUES (?, 1, 1, 100.0)
            #         ON CONFLICT(id) DO UPDATE SET
            #             total_game_num = total_game_num + 1,
            #             won_game_num = won_game_num + 1,
            #             win_rate = ROUND((won_game_num + 1) * 100.0 / (total_game_num + 1), 2)
            #     ''', (steam_id,))
            # else:
            #     # is not winner
            #     db.execute('''
            #         INSERT INTO Players (id, total_game_num, won_game_num, win_rate)
            #         VALUES (?, 1, 0, 0.0)
            #         ON CONFLICT(id) DO UPDATE SET
            #             total_game_num = total_game_num + 1,
            #             win_rate = ROUND(won_game_num * 100.0 / (total_game_num + 1), 2)
            #     ''', (steam_id,))
            
            # gameplayer data
            db.execute('''
                INSERT INTO GamePlayers (
                    game_id, player_id, team, is_winner, 
                    leader_type, civilization_type, player_code
                ) VALUES (?, ?, ?, ?, ?, ?);
            ''', (
                game_id,
                steam_id,
                player_info.get('team'),
                is_winner,
                player_info.get('leader_type'),
                player_info.get('civilization_type'),
                player_code
            ))
            
            
        
        db.commit()
        _Debug(f"Save game data successfully!")
        close_db()
        return game_id or 0
        
        
    except sqlite3.Error as e:
        db.rollback()
        _Debug(f"Error when saving game data: {e}")
        raise


def find_duplicate_game_by_timestamp(db: sqlite3.Connection, timestamp: int, tolerance_seconds: int = 10) -> dict | None:
    """
    根据时间戳查找重复游戏（支持时间容差）
    
    Args:
        db: 数据库连接
        timestamp: 要检查的时间戳
        tolerance_seconds: 时间容差（秒）
        
    Returns:
        重复的游戏记录或None
    """
    # 计算时间范围
    min_timestamp = timestamp - tolerance_seconds
    max_timestamp = timestamp + tolerance_seconds
    
    # # 将时间戳范围转换为日期时间字符串范围
    # # from datetime import datetime
    # min_time_str = datetime.fromtimestamp(min_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    # max_time_str = datetime.fromtimestamp(max_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    # 查询在时间范围内的游戏
    existing_game = db.execute('''
        SELECT id, game_time_stamp 
        FROM Games 
        WHERE game_time_stamp BETWEEN ? AND ?
    ''', (min_timestamp, max_timestamp)).fetchone()
    
    return existing_game

def validate_game_data(game_data: dict[str, any]) -> any: # type: ignore
    # ignore less than 33 (including 33)
    if not DEBUG and game_data.get('player_num', 0) < 8:
        return None
    return game_data

# Database mothods
def get_db() -> sqlite3.Connection:
    '''
    get database
    '''
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
        _Debug('Connect with database successfully')
    
    return g.db

def init_db():
    '''
    initialize database
    NOTICE: will drop old tables!!!
    '''
    db = get_db()
    sql_script: str
    with open('sql/init_db.sql', 'r', encoding='utf-8') as init_db_sql:
        sql_script = init_db_sql.read()
    db.executescript(sql_script)
    db.commit()
    _Debug('Initialize database successfully')
    
def close_db():
    if hasattr(g, 'db'):
        g.db.close()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host=HOST, port=PORT, debug=DEBUG)