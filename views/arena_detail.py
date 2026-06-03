import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def arena_detail_view(page: ft.Page, team_id: int):

    def load_team():
        con = get_connection()
        result = con.execute(
            "SELECT id, name FROM arena_defense_team WHERE id = ?", [team_id]
        ).fetchone()
        con.close()
        return result

    def load_team_cookies():
        con = get_connection()
        result = con.execute(
            """
            SELECT c.name, t.name AS topping_name, b.name AS biscuit_name
            FROM arena_team_cookie atc
            JOIN cookie c ON atc.cookie_id = c.id
            LEFT JOIN topping t ON atc.topping_id = t.id
            LEFT JOIN biscuit b ON atc.biscuit_id = b.id
            WHERE atc.team_id = ?
            """,
            [team_id],
        ).fetchall()
        con.close()
        return result

    team = load_team()

    if not team:
        return ft.View(
            route=f"/arena/{team_id}",
            controls=[ft.Text("아레나 방어 팀 정보를 찾을 수 없습니다.")],
        )

    t_id, name = team
    cookies = load_team_cookies()

    def cookie_card(cookie):
        c_name, topping_name, biscuit_name = cookie
        return ft.Card(
            content=ft.Container(
                padding=12,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.FACE, size=60),
                        ft.Text(
                            c_name,
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(),
                        ft.Text(
                            f"토핑: {topping_name if topping_name else '-'}", size=11
                        ),
                        ft.Text(
                            f"비스킷: {biscuit_name if biscuit_name else '-'}", size=11
                        ),
                    ],
                ),
            )
        )

    return ft.View(
        route=f"/arena/{team_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 6),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/arena"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            name, size=22, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            "쿠키 구성",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Divider(),
                                        ft.Row(
                                            controls=[cookie_card(c) for c in cookies],
                                            wrap=True,
                                            spacing=10,
                                            run_spacing=10,
                                        )
                                        if cookies
                                        else ft.Text(
                                            "쿠키 구성 정보가 없습니다.",
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
