import flet as ft
from db.database import get_connection


def sidebar(page):
    """사이드바 네비게이션 메뉴를 반환하는 함수"""
    def nav(route):
        page.go(route)
    return ft.Container(
        width=150,
        bgcolor="#1a1a2e",
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("Kingdom\nDeck Builder", size=16, weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                    padding=20,
                ),
                ft.Divider(color="white24"),
                ft.TextButton("쿠키", on_click=lambda e: nav("/cookies"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("타르트", on_click=lambda e: nav("/toppings"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("비스킷", on_click=lambda e: nav("/biscuits"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("보물", on_click=lambda e: nav("/treasures"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("컨텐츠", on_click=lambda e: nav("/contents"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("몬스터", on_click=lambda e: nav("/monsters"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("아레나 방어팀", on_click=lambda e: nav("/arena"), style=ft.ButtonStyle(color="white")),
                ft.TextButton("팀편성", on_click=lambda e: nav("/team"), style=ft.ButtonStyle(color="white")),
            ],
            spacing=0,
        ),
    )


def team_build_view(page: ft.Page):
    """팀 편성 화면을 반환하는 함수"""
    con = get_connection()

    # 드롭다운 옵션용 데이터 조회
    cookies = con.execute("SELECT cookie_id, cookie_name FROM cookie ORDER BY cookie_name").fetchall()
    tarts = con.execute("SELECT tart_id, tart_name FROM tart ORDER BY tart_name").fetchall()
    biscuits = con.execute("SELECT biscuit_id, biscuit_name FROM biscuit ORDER BY biscuit_name").fetchall()
    treasures = con.execute("SELECT treasure_id, treasure_name FROM treasure ORDER BY treasure_name").fetchall()
    contents = con.execute("SELECT content_id, content_name FROM content ORDER BY content_name").fetchall()

    # 드롭다운 옵션 생성
    cookie_options = [ft.dropdown.Option(str(c[0]), c[1]) for c in cookies]
    tart_options = [ft.dropdown.Option(str(t[0]), t[1]) for t in tarts]
    biscuit_options = [ft.dropdown.Option(str(b[0]), b[1]) for b in biscuits]
    treasure_options = [ft.dropdown.Option(str(t[0]), t[1]) for t in treasures]
    content_options = [ft.dropdown.Option(str(c[0]), c[1]) for c in contents]

    # 컨텐츠 선택 드롭다운 및 팀 이름 입력 필드
    content_dd = ft.Dropdown(label="컨텐츠 선택", options=content_options, width=300)
    team_name_field = ft.TextField(label="팀 이름 입력", width=200)

    # 슬롯 5개 생성 (각 슬롯은 쿠키, 레벨, 별, 초월, 토핑, 비스킷 선택 드롭다운 포함)
    slots = []
    for i in range(5):
        slots.append({
            "cookie": ft.Dropdown(label="쿠키 선택", options=cookie_options, width=150),
            "level": ft.Dropdown(label="레벨", options=[ft.dropdown.Option(str(v)) for v in range(1, 101)], width=80),
            "star": ft.Dropdown(label="별", options=[ft.dropdown.Option(str(v)) for v in range(0, 6)], width=80),
            "transcendence": ft.Dropdown(label="초월", options=[ft.dropdown.Option(str(v)) for v in range(0, 6)], width=80),
            "tart": ft.Dropdown(label="토핑", options=tart_options, width=150),
            "biscuit": ft.Dropdown(label="비스킷", options=biscuit_options, width=150),
        })

    # 보물 선택 드롭다운 3개
    treasure_dds = [
        ft.Dropdown(label=f"보물 {i+1}", options=treasure_options, width=150)
        for i in range(3)
    ]

    def save_team(e):
        """팀 편성 저장 버튼 클릭 시 DuckDB에 팀 정보를 저장하는 함수"""
        con2 = get_connection()

        # 팀 ID 자동 증가
        team_id = con2.execute("SELECT COALESCE(MAX(team_id), 0) + 1 FROM team").fetchone()[0]
        content_id = int(content_dd.value) if content_dd.value else None

        # team 테이블에 팀 기본 정보 삽입
        con2.execute(
            "INSERT INTO team VALUES (?, ?, NULL, CURRENT_TIMESTAMP, ?)",
            [team_id, team_name_field.value or f"팀 {team_id}", content_id]
        )

        # 슬롯별 쿠키 구성 삽입
        for i, slot in enumerate(slots):
            if slot["cookie"].value:
                # team_cookie ID 자동 증가
                tc_id = con2.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM team_cookie").fetchone()[0]
                con2.execute(
                    "INSERT INTO team_cookie VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [
                        tc_id,
                        int(slot["level"].value) if slot["level"].value else 1,
                        int(slot["star"].value) if slot["star"].value else 0,
                        int(slot["transcendence"].value) if slot["transcendence"].value else 0,
                        i + 1,  # 슬롯 번호 (1~5)
                        team_id,
                        int(slot["cookie"].value),
                        int(slot["tart"].value) if slot["tart"].value else None,
                        int(slot["biscuit"].value) if slot["biscuit"].value else None,
                    ]
                )

        con2.close()
        # 저장 완료 후 저장된 팀 편성 화면으로 이동
        page.go("/team/save")

    # 슬롯 행 UI 생성
    slot_rows = []
    for i, slot in enumerate(slots):
        slot_rows.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"슬롯{i+1}", width=50),
                        slot["cookie"],
                        slot["level"],
                        slot["star"],
                        slot["transcendence"],
                        slot["tart"],
                        slot["biscuit"],
                    ],
                    spacing=8,
                ),
                padding=ft.Padding(left=0, right=0, top=4, bottom=4),
            )
        )

    return ft.View(
        route="/team",
        padding=0,
        controls=[
            ft.Row(
                controls=[
                    sidebar(page),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text("Kingdom Deck Builder", size=20, weight=ft.FontWeight.BOLD),
                                padding=16,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                # 팀편성 및 컨텐츠 선택
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("팀편성", size=16, weight=ft.FontWeight.BOLD),
                                                        content_dd,
                                                    ],
                                                    spacing=8,
                                                ),
                                                # 보물 선택 (최대 3개)
                                                ft.Column(
                                                    controls=[
                                                        ft.Text("보물 선택(최대 3개)", size=16, weight=ft.FontWeight.BOLD),
                                                        ft.Row(controls=treasure_dds, spacing=8),
                                                    ],
                                                    spacing=8,
                                                ),
                                            ],
                                            spacing=40,
                                        ),
                                        ft.Divider(),
                                        ft.Text("쿠키편성(최대 5명)", size=14, weight=ft.FontWeight.BOLD),
                                        *slot_rows,
                                        ft.Divider(),
                                        # 팀 이름 입력 및 저장 버튼
                                        ft.Row(
                                            controls=[
                                                team_name_field,
                                                ft.ElevatedButton("팀 편성 저장", on_click=save_team),
                                            ],
                                            spacing=16,
                                        ),
                                    ],
                                    spacing=8,
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                                expand=True,
                                padding=16,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        ],
    )