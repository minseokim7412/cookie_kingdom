import duckdb
import os

DB_PATH = "data/ckk.duckdb"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return duckdb.connect(DB_PATH)


def init_db():
    con = get_connection()

    con.execute("""
        CREATE TABLE IF NOT EXISTS cookie (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            grade VARCHAR,
            attribute VARCHAR,
            position VARCHAR,
            cookie_type VARCHAR,
            skill_name VARCHAR,
            skill_description VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS topping (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            topping_type VARCHAR,
            main_stat VARCHAR,
            sub_stat VARCHAR,
            set_effect VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS biscuit (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            grade VARCHAR,
            stat VARCHAR,
            effect VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS treasure (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            grade VARCHAR,
            stat VARCHAR,
            effect VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            content_type VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS monster (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            hp INTEGER,
            attribute VARCHAR,
            weak_attribute VARCHAR,
            image_path VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS content_monster (
            id INTEGER PRIMARY KEY,
            content_id INTEGER,
            monster_id INTEGER
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS arena_defense_team (
            id INTEGER PRIMARY KEY,
            name VARCHAR
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS arena_team_cookie (
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            cookie_id INTEGER,
            topping_id INTEGER,
            biscuit_id INTEGER
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            content_id INTEGER,
            memo VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS team_cookie (
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            cookie_id INTEGER,
            topping_id INTEGER,
            biscuit_id INTEGER,
            treasure_id INTEGER,
            level INTEGER,
            star INTEGER,
            transcendence INTEGER
        )
    """)

    con.close()
    print("DB 초기화 완료!")
    insert_sample_data()


def insert_sample_data():
    con = get_connection()

    con.execute("""
        INSERT OR IGNORE INTO cookie VALUES
        (1, '홍차 쿠키', '에픽', '불', '후방', '마법형', '홍차 파티', '적 전체에 불 속성 피해를 입힌다.', NULL),
        (2, '마들렌 쿠키', '에픽', '빛', '전방', '돌격형', '성스러운 방패', '아군 전체의 방어력을 높인다.', NULL),
        (3, '독버섯 쿠키', '에픽', '독', '중방', '침투형', '독버섯 포자', '적에게 독 속성 피해를 입힌다.', NULL)
    """)

    con.execute("""
        INSERT OR IGNORE INTO topping VALUES
        (1, '아몬드 토핑', '아몬드', '공격력 +5%', '치명타 확률 +1%', '공격력 세트 효과', NULL),
        (2, '젤리워치 토핑', '젤리워치', '쿨타임 -5%', '공격력 +1%', '쿨타임 세트 효과', NULL),
        (3, '초코칩 토핑', '초코칩', '방어력 +5%', 'HP +1%', '방어력 세트 효과', NULL)
    """)

    con.execute("""
        INSERT OR IGNORE INTO biscuit VALUES
        (1, '용감한 쿠키의 비스킷', '일반', '공격력 +3%', '전방 쿠키 공격력 증가', NULL),
        (2, '마법사의 비스킷', '희귀', '마법 공격력 +5%', '마법형 쿠키 쿨타임 감소', NULL)
    """)

    con.execute("""
        INSERT OR IGNORE INTO treasure VALUES
        (1, '老트리의 지혜', '에픽', '모든 능력치 +3%', '전체 쿠키 버프', NULL),
        (2, '무지개 조개 팬던트', '희귀', 'HP +5%', 'HP 회복량 증가', NULL)
    """)

    con.execute("""
        INSERT OR IGNORE INTO content VALUES
        (1, '킹덤 아레나', 'arena'),
        (2, '월드 탐험', 'monster'),
        (3, '케이크 타워', 'monster'),
        (4, '길드 토벌전', 'monster'),
        (5, '수호의 성전', 'monster'),
        (6, '증명의 전장', 'monster')
    """)

    con.execute("""
        INSERT OR IGNORE INTO monster VALUES
        (1, '해골 전사', 5000, '어둠', '빛', NULL),
        (2, '불꽃 골렘', 8000, '불', '얼음', NULL),
        (3, '독거미', 3000, '독', '불', NULL)
    """)

    con.execute("""
        INSERT OR IGNORE INTO content_monster VALUES
        (1, 2, 1),
        (2, 2, 2),
        (3, 3, 3)
    """)

    con.close()
    print("샘플 데이터 삽입 완료!")
