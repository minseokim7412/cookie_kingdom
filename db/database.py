import duckdb
import os

# DuckDB 파일 경로
DB_PATH = "data/ckk.duckdb"


def get_connection():
    """DuckDB 연결을 반환하는 함수"""
    os.makedirs("data", exist_ok=True)
    return duckdb.connect(DB_PATH)


def init_db():
    """데이터베이스 테이블을 초기화하는 함수"""
    con = get_connection()

    # 등급 테이블 (ANCIENT, LEGENDARY, EPIC, RARE, COMMON, BEAST)
    con.execute("""
        CREATE TABLE IF NOT EXISTS grade (
            grade_code VARCHAR PRIMARY KEY,
            grade_name VARCHAR NOT NULL
        )
    """)

    # 속성 테이블 (어둠, 불꽃, 물, 자연, 빛, 마법, 무속성)
    con.execute("""
        CREATE TABLE IF NOT EXISTS attribute (
            attribute_name VARCHAR PRIMARY KEY
        )
    """)

    # 포지션 테이블 (선봉, 중단, 후방)
    con.execute("""
        CREATE TABLE IF NOT EXISTS position (
            position_name VARCHAR PRIMARY KEY
        )
    """)

    # 쿠키 유형 테이블 (돌격형, 마법형, 치유형 등)
    con.execute("""
        CREATE TABLE IF NOT EXISTS cookie_type (
            cookie_type_name VARCHAR PRIMARY KEY
        )
    """)

    # 타르트 유형 테이블 (공격형, 방어형, 체력형, 쿨타임형)
    con.execute("""
        CREATE TABLE IF NOT EXISTS tart_type (
            tart_type_name VARCHAR PRIMARY KEY
        )
    """)

    # 컨텐츠 유형 테이블 (아레나, 월드탐험, 길드토벌 등)
    con.execute("""
        CREATE TABLE IF NOT EXISTS content_type (
            content_type_name VARCHAR PRIMARY KEY
        )
    """)

    # 시리즈 테이블 (보물의 시리즈 정보)
    con.execute("""
        CREATE TABLE IF NOT EXISTS series (
            series_name VARCHAR PRIMARY KEY
        )
    """)

    # 쿠키 테이블 - grade, attribute, position, cookie_type 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS cookie (
            cookie_id BIGINT PRIMARY KEY,
            cookie_name VARCHAR NOT NULL,
            image_path VARCHAR,
            grade_code VARCHAR REFERENCES grade(grade_code),
            attribute_name VARCHAR REFERENCES attribute(attribute_name),
            position_name VARCHAR REFERENCES position(position_name),
            cookie_type_name VARCHAR REFERENCES cookie_type(cookie_type_name)
        )
    """)

    # 타르트 테이블 - grade, tart_type 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS tart (
            tart_id BIGINT PRIMARY KEY,
            tart_name VARCHAR NOT NULL,
            stat DECIMAL,
            set_effect VARCHAR,
            image_path VARCHAR,
            grade_code VARCHAR REFERENCES grade(grade_code),
            tart_type_name VARCHAR REFERENCES tart_type(tart_type_name)
        )
    """)

    # 비스킷 테이블 - grade 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS biscuit (
            biscuit_id BIGINT PRIMARY KEY,
            biscuit_name VARCHAR NOT NULL,
            level SMALLINT,
            atk SMALLINT,
            hp SMALLINT,
            extra_stat TEXT,
            image_path VARCHAR,
            grade_code VARCHAR REFERENCES grade(grade_code)
        )
    """)

    # 보물 테이블 - grade, series 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS treasure (
            treasure_id BIGINT PRIMARY KEY,
            treasure_name VARCHAR NOT NULL,
            level SMALLINT,
            cur_ability TEXT,
            next_ability TEXT,
            image_path VARCHAR,
            grade_code VARCHAR REFERENCES grade(grade_code),
            series_name VARCHAR REFERENCES series(series_name)
        )
    """)

    # 컨텐츠 테이블 - content_type 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS content (
            content_id BIGINT PRIMARY KEY,
            content_name VARCHAR NOT NULL,
            image_path VARCHAR,
            content_type_name VARCHAR REFERENCES content_type(content_type_name)
        )
    """)

    # 몬스터 테이블
    con.execute("""
        CREATE TABLE IF NOT EXISTS monster (
            monster_id BIGINT PRIMARY KEY,
            monster_name VARCHAR NOT NULL,
            hp INT,
            power INT,
            atk INT,
            def INT,
            image_path VARCHAR
        )
    """)

    # 컨텐츠-몬스터 관계 테이블 (다대다 관계)
    con.execute("""
        CREATE TABLE IF NOT EXISTS content_monster (
            id BIGINT PRIMARY KEY,
            content_id BIGINT REFERENCES content(content_id),
            monster_id BIGINT REFERENCES monster(monster_id)
        )
    """)

    # 팀 테이블 - content 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS team (
            team_id BIGINT PRIMARY KEY,
            team_name VARCHAR NOT NULL,
            memo TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            content_id BIGINT REFERENCES content(content_id)
        )
    """)

    # 팀 쿠키 구성 테이블 - team, cookie, tart, biscuit 테이블을 외래키로 참조
    con.execute("""
        CREATE TABLE IF NOT EXISTS team_cookie (
            id BIGINT PRIMARY KEY,
            level INT,
            star INT,
            transcendence INT,
            slot_no INT,
            team_id BIGINT REFERENCES team(team_id),
            cookie_id BIGINT REFERENCES cookie(cookie_id),
            tart_id BIGINT REFERENCES tart(tart_id),
            biscuit_id BIGINT REFERENCES biscuit(biscuit_id)
        )
    """)

    # 아레나 방어팀 테이블
    con.execute("""
        CREATE TABLE IF NOT EXISTS arena_defense_team (
            team_id BIGINT PRIMARY KEY,
            user_name VARCHAR,
            memo TEXT
        )
    """)

    # 아레나 방어팀 쿠키 구성 테이블
    con.execute("""
        CREATE TABLE IF NOT EXISTS arena_team_cookie (
            id BIGINT PRIMARY KEY,
            slot_no INT,
            team_id BIGINT REFERENCES arena_defense_team(team_id),
            cookie_id BIGINT REFERENCES cookie(cookie_id),
            tart_id BIGINT REFERENCES tart(tart_id),
            biscuit_id BIGINT REFERENCES biscuit(biscuit_id)
        )
    """)

    # 아레나 방어팀 보물 구성 테이블
    con.execute("""
        CREATE TABLE IF NOT EXISTS arena_team_treasure (
            id BIGINT PRIMARY KEY,
            slot_no INT,
            team_id BIGINT REFERENCES arena_defense_team(team_id),
            treasure_id BIGINT REFERENCES treasure(treasure_id)
        )
    """)

    con.close()
    print("DB 초기화 완료!")
    insert_sample_data()


def insert_sample_data():
    """샘플 데이터를 삽입하는 함수"""
    con = get_connection()

    # 등급 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO grade VALUES
        ('ANCIENT', '에인션트'),
        ('LEGENDARY', '레전더리'),
        ('EPIC', '에픽'),
        ('RARE', '레어'),
        ('COMMON', '커먼'),
        ('BEAST', '비스트')
    """)

    # 속성 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO attribute VALUES
        ('어둠'), ('불꽃'), ('물'), ('자연'), ('빛'), ('마법'), ('무속성')
    """)

    # 포지션 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO position VALUES
        ('선봉'), ('중단'), ('후방')
    """)

    # 쿠키 유형 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO cookie_type VALUES
        ('돌격형'), ('마법형'), ('치유형'), ('방어형'), ('지원형'), ('폭발형'), ('침투형')
    """)

    # 타르트 유형 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO tart_type VALUES
        ('공격형'), ('방어형'), ('체력형'), ('쿨타임형')
    """)

    # 컨텐츠 유형 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO content_type VALUES
        ('아레나'), ('월드탐험'), ('길드토벌'), ('케이크타워'), ('수호의성전')
    """)

    # 시리즈 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO series VALUES
        ('용감한 쿠키 시리즈'), ('마법사 시리즈'), ('왕국 시리즈'), ('자연 시리즈'), ('빛의 시리즈')
    """)

    # 쿠키 데이터 삽입 (실제 쿠키런 킹덤 데이터 기반)
    con.execute("""
        INSERT OR IGNORE INTO cookie VALUES
        (1,  '바다요정 쿠키',     'cookies/cookie_1.png',  'LEGENDARY', '물',   '중단', '마법형'),
        (2,  '퓨어바닐라 쿠키',   'cookies/cookie_2.png',  'LEGENDARY', '빛',   '후방', '치유형'),
        (3,  '마들렌 쿠키',       'cookies/cookie_3.png',  'EPIC',      '빛',   '선봉', '방어형'),
        (4,  '에스프레소 쿠키',   'cookies/cookie_4.png',  'EPIC',      '마법', '중단', '마법형'),
        (5,  '미스틱플라워 쿠키', 'cookies/cookie_5.png',  'BEAST',     '자연', '후방', '치유형'),
        (6,  '버닝스파이스 쿠키', 'cookies/cookie_6.png',  'BEAST',     '불꽃', '선봉', '돌격형'),
        (7,  '쉐도우밀크 쿠키',   'cookies/cookie_7.png',  'BEAST',     '어둠', '중단', '마법형'),
        (8,  '홀리베리 쿠키',     'cookies/cookie_8.png',  'LEGENDARY', '빛',   '선봉', '방어형'),
        (9,  '골드치즈 쿠키',     'cookies/cookie_9.png',  'LEGENDARY', '빛',   '후방', '지원형'),
        (10, '세인트릴리 쿠키',   'cookies/cookie_10.png', 'LEGENDARY', '빛',   '후방', '치유형'),
        (11, '어둠마녀 쿠키',     'cookies/cookie_11.png', 'EPIC',      '어둠', '후방', '마법형')
    """)

    # 타르트 데이터 삽입 (실제 쿠키런 킹덤 데이터 기반)
    con.execute("""
        INSERT OR IGNORE INTO tart VALUES
        (1, '고급 단단한 아몬드 타르트',      11.3, '아몬드 토핑 세트',    'toppings/tart_1.png', 'EPIC', '공격형'),
        (2, '고급 과즙팡팡 애플젤리 타르트',   5.0,  '애플젤리 토핑 세트',  'toppings/tart_2.png', 'EPIC', '쿨타임형'),
        (3, '고급 딱딱한 호두 타르트',         18.7, '호두 토핑 세트',      'toppings/tart_3.png', 'EPIC', '방어형'),
        (4, '고급 화끈화끈 라즈베리 타르트',    3.6,  '라즈베리 토핑 세트',  'toppings/tart_4.png', 'EPIC', '공격형'),
        (5, '고급 건강한 땅콩 타르트',         10.6, '땅콩 토핑 세트',      'toppings/tart_5.png', 'EPIC', '체력형')
    """)

    # 비스킷 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO biscuit VALUES
        (1, '전설 짜릿한 비스킷',  1, 486, 0,    '전체 쿠키 공격력 증가',  'biscuits/biscuit_1.png', 'LEGENDARY'),
        (2, '에픽 짜릿한 비스킷',  1, 324, 0,    '전체 쿠키 공격력 증가',  'biscuits/biscuit_2.png', 'EPIC'),
        (3, '전설 바삭한 비스킷',  1, 0,   2430, '전체 쿠키 방어력 증가',  'biscuits/biscuit_3.png', 'LEGENDARY'),
        (4, '전설 상쾌한 비스킷',  1, 0,   0,    '전체 쿠키 쿨타임 감소',  'biscuits/biscuit_4.png', 'LEGENDARY'),
        (5, '에픽 쫀득한 비스킷',  1, 0,   1620, '전체 쿠키 HP 증가',     'biscuits/biscuit_5.png', 'EPIC')
    """)

    # 보물 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO treasure VALUES
        (1, '무녀맛 쿠키의 영험한 종이부적',           1, '전체 쿠키 스킬 피해 +12%', '전체 쿠키 스킬 피해 +15%', 'treasures/treasure_1.png', 'EPIC',      '왕국 시리즈'),
        (2, '아이스크림 상인 유령의 신기루 아이스크림',  1, '전체 쿠키 HP +5%',        '전체 쿠키 HP +6%',         'treasures/treasure_2.png', 'EPIC',      '자연 시리즈'),
        (3, '꿈을 달리는 차장의 별빛 호루라기',         1, '전체 쿠키 공격력 +8%',     '전체 쿠키 공격력 +10%',    'treasures/treasure_3.png', 'LEGENDARY', '빛의 시리즈'),
        (4, '꿈꾸는 곰젤리의 반짝반짝 젤리시계',        1, '전체 쿠키 쿨타임 -10%',    '전체 쿠키 쿨타임 -12%',    'treasures/treasure_4.png', 'EPIC',      '마법사 시리즈'),
        (5, '사나운 모래 폭풍이 담긴 유리병',           1, '전체 쿠키 방어력 +15%',    '전체 쿠키 방어력 +18%',    'treasures/treasure_5.png', 'EPIC',      '왕국 시리즈')
    """)

    # 컨텐츠 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO content VALUES
        (1, '킹덤 아레나', NULL, '아레나'),
        (2, '월드 탐험',   NULL, '월드탐험'),
        (3, '케이크 타워', NULL, '케이크타워'),
        (4, '길드 토벌전', NULL, '길드토벌'),
        (5, '수호의 성전', NULL, '수호의성전')
    """)

    # 몬스터 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO monster VALUES
        (1,  '해골 전사',              5000,  1200, 306,  150,  NULL),
        (2,  '불꽃 골렘',              8000,  2500, 520,  300,  NULL),
        (3,  '독거미',                 3000,  900,  210,  80,   NULL),
        (4,  '초코크림 늑대 망치맨',   9575,  2333, 306,  1225, NULL),
        (5,  '숙련된 생크림 롤멧돼지', 11645, 2589, 209,  1862, NULL),
        (6,  '용곰틀이',               22005, 4128, 620,  3909, NULL),
        (7,  '은행강도 두목',           24087, 3905, 618,  1832, NULL),
        (8,  '어둠의 기사',             15000, 3200, 480,  2100, NULL),
        (9,  '마법 골렘',               18000, 3800, 540,  2500, NULL),
        (10, '화염 드래곤',             30000, 5500, 800,  4500, NULL)
    """)

    # 컨텐츠-몬스터 관계 데이터 삽입
    con.execute("""
        INSERT OR IGNORE INTO content_monster VALUES
        (1,  2, 1),
        (2,  2, 2),
        (3,  2, 4),
        (4,  2, 5),
        (5,  3, 6),
        (6,  3, 7),
        (7,  4, 8),
        (8,  4, 9),
        (9,  5, 10),
        (10, 5, 3)
    """)

    con.close()
    print("샘플 데이터 삽입 완료!")