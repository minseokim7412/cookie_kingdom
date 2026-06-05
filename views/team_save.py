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


def team_save_view(page: ft.Page):
    con = get_connection()

    def load_teams():
        return con.execute(
            """
            SELECT t.team_id, t.team_name, c.content_name, t.created_at
            FROM team t
            LEFT JOIN content c ON t.content_id = c.content_id
            ORDER BY t.team_id DESC
            """
        ).fetchall()

    def delete_team(team_id):
        con2 = get_connection()
        con2.execute("DELETE FROM team_cookie WHERE team_id = ?", [team_id])
        con2.execute("DELETE FROM team WHERE team_id = ?", [team_id])
        con2.close()
        refresh()

    list_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=8)

    def build_list(rows):
        items = []
        for row in rows:
            team_id, team_name, content_name, created_at = row
            created_str = str(created_at)[:10] if created_at else "-"
            items.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(team_name or f"팀 {team_id}", size=15, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"컨텐츠 : {content_name or '-'}", size=13),
                                    ft.Text(f"저장일 : {created_str}", size=12, color="grey"),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.ElevatedButton("불러오기", on_click=lambda e, tid=team_id: page.go(f"/team?load={tid}")),
                                    ft.ElevatedButton("삭제", on_click=lambda e, tid=team_id: delete_team(tid), bgcolor="red", color="white"),
                                ],
                                spacing=4,
                            ),
                        ],
                    ),
                    padding=16,
                    border=ft.Border(
                        top=ft.BorderSide(1, "#333333"),
                        bottom=ft.BorderSide(1, "#333333"),
                        left=ft.BorderSide(1, "#333333"),
                        right=ft.BorderSide(1, "#333333"),
                    ),
                    border_radius=8,
                )
            )
        return items

    def refresh():
        rows = load_teams()
        list_column.controls = build_list(rows) if rows else [ft.Text("저장된 팀 편성이 없습니다.", color="grey")]
        page.update()

    refresh()

    return ft.View(
        route="/team/save",
        padding=0,
        controls=[
            ft.Row(
                controls=[
                    sidebar(page),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton("← 팀편성으로", on_click=lambda e: page.go("/team")),
                                padding=16,
                            ),
                            ft.Container(
                                content=ft.Text("저장된 팀 편성", size=18, weight=ft.FontWeight.BOLD),
                                padding=ft.Padding(left=16, right=16, top=0, bottom=8),
                            ),
                            ft.Container(
                                content=list_column,
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