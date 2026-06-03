import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def team_save_view(page: ft.Page, team_data: dict = None):

    def load_saved_teams():
        con = get_connection()
        result = con.execute(
            """
            SELECT t.id, t.name, t.memo, t.created_at, c.name AS content_name
            FROM team t
            LEFT JOIN content c ON t.content_id = c.id
            ORDER BY t.created_at DESC
            """
        ).fetchall()
        con.close()
        return result

    def delete_team(team_id):
        con = get_connection()
        con.execute("DELETE FROM team_cookie WHERE team_id = ?", [team_id])
        con.execute("DELETE FROM team WHERE id = ?", [team_id])
        con.close()
        refresh_list()

    def team_row(team):
        t_id, t_name, t_memo, t_created, t_content = team
        return ft.Card(
            content=ft.Container(
                padding=12,
                content=ft.Row(
                    controls=[
                        ft.Column(
                            expand=True,
                            controls=[
                                ft.Text(
                                    t_name if t_name else "이름 없음",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"컨텐츠: {t_content if t_content else '-'}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Text(
                                    f"메모: {t_memo if t_memo else '-'}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                ),
                                ft.Text(
                                    f"저장일: {str(t_created)[:19] if t_created else '-'}",
                                    size=11,
                                    color=ft.Colors.GREY_400,
                                ),
                            ],
                            spacing=4,
                        ),
                        ft.Column(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Text("불러오기"),
                                    on_click=lambda e, tid=t_id: page.go(
                                        f"/team/{tid}"
                                    ),
                                ),
                                ft.ElevatedButton(
                                    content=ft.Text("삭제"),
                                    on_click=lambda e, tid=t_id: delete_team(tid),
                                ),
                            ],
                            spacing=8,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )

    saved_teams_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=10)

    def refresh_list():
        saved_teams_column.controls.clear()
        teams = load_saved_teams()
        if teams:
            for t in teams:
                saved_teams_column.controls.append(team_row(t))
        else:
            saved_teams_column.controls.append(
                ft.Text("저장된 팀 편성이 없습니다.", color=ft.Colors.GREY_600)
            )
        page.update()

    refresh_list()

    return ft.View(
        route="/team/save",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 7),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 팀 편성으로"),
                                    on_click=lambda e: page.go("/team"),
                                ),
                                padding=10,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "저장된 팀 편성", size=22, weight=ft.FontWeight.BOLD
                                ),
                                padding=ft.padding.only(left=20),
                            ),
                            ft.Divider(),
                            saved_teams_column,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
