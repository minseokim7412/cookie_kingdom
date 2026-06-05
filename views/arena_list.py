import flet as ft
from db.database import get_connection


def sidebar(page):
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


def arena_list_view(page: ft.Page):
    con = get_connection()

    def load_teams(search=""):
        return con.execute(
            "SELECT team_id, user_name, memo FROM arena_defense_team WHERE user_name LIKE ? ORDER BY team_id",
            [f"%{search}%"]
        ).fetchall()

    def get_team_cookies(team_id):
        return con.execute(
            """
            SELECT c.cookie_name
            FROM arena_team_cookie atc
            JOIN cookie c ON atc.cookie_id = c.cookie_id
            WHERE atc.team_id = ?
            ORDER BY atc.slot_no
            """,
            [team_id]
        ).fetchall()

    def get_team_treasures(team_id):
        return con.execute(
            """
            SELECT t.treasure_name
            FROM arena_team_treasure att
            JOIN treasure t ON att.treasure_id = t.treasure_id
            WHERE att.team_id = ?
            ORDER BY att.slot_no
            """,
            [team_id]
        ).fetchall()

    def build_list(rows):
        items = []
        for row in rows:
            team_id, user_name, memo = row
            cookies = get_team_cookies(team_id)
            treasures = get_team_treasures(team_id)
            cookie_text = ", ".join([c[0] for c in cookies]) if cookies else "-"
            treasure_text = ", ".join([t[0] for t in treasures]) if treasures else "-"
            items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("방어팀 유저이름", size=11, color="grey"),
                                    ft.Text(user_name or "-", size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"보물 : {treasure_text}", size=12),
                                    ft.Text(memo or "-", size=12, color="grey"),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(f"쿠키 구성 : {cookie_text}", size=12),
                                ],
                                expand=True,
                            ),
                        ],
                    ),
                    padding=16,
                    border=ft.Border(bottom=ft.BorderSide(1, "#333333")),
                )
            )
        return items

    list_column = ft.Column(scroll=ft.ScrollMode.AUTO)

    def refresh(search=""):
        rows = load_teams(search)
        list_column.controls = build_list(rows) if rows else [ft.Text("방어팀 데이터가 없습니다.", color="grey")]
        page.update()

    def on_search(e):
        refresh(e.control.value)

    refresh()

    return ft.View(
        route="/arena",
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
                                content=ft.Row(
                                    controls=[
                                        ft.TextField(hint_text="방어팀 검색", expand=True, on_change=on_search, prefix_icon=ft.Icons.SEARCH),
                                        ft.ElevatedButton("필터 ▼"),
                                    ]
                                ),
                                padding=ft.Padding(left=16, right=16, top=0, bottom=0),
                            ),
                            ft.Container(content=list_column, expand=True, padding=16),
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