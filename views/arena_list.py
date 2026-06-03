import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def arena_list_view(page: ft.Page):

    def load_arena_teams(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name FROM arena_defense_team WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute("SELECT id, name FROM arena_defense_team").fetchall()
        con.close()
        return result

    def load_team_cookies(team_id):
        con = get_connection()
        result = con.execute(
            """
            SELECT c.name FROM arena_team_cookie atc
            JOIN cookie c ON atc.cookie_id = c.id
            WHERE atc.team_id = ?
            """,
            [team_id],
        ).fetchall()
        con.close()
        return [r[0] for r in result]

    def arena_row(team):
        team_id, name = team
        cookies = load_team_cookies(team_id)
        cookie_names = ", ".join(cookies) if cookies else "쿠키 정보 없음"
        return ft.GestureDetector(
            on_tap=lambda e, tid=team_id: page.go(f"/arena/{tid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SECURITY, size=40, color=ft.Colors.BLUE_400),
                        ft.Column(
                            controls=[
                                ft.Text(name, size=14, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f"쿠키 구성: {cookie_names}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=12, bottom=12, left=16, right=16),
                border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
            ),
        )

    search_field = ft.TextField(
        hint_text="🔍 방어 팀 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    arena_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        arena_list.controls.clear()
        teams = load_arena_teams(keyword)
        for t in teams:
            arena_list.controls.append(arena_row(t))
        page.update()

    refresh_list()

    return ft.View(
        route="/arena",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 6),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            arena_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
