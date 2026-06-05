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


def treasure_detail_view(page: ft.Page, treasure_id: int):
    con = get_connection()

    row = con.execute(
        """
        SELECT t.treasure_id, t.treasure_name, t.image_path,
               t.grade_code, g.grade_name,
               t.level, t.cur_ability, t.next_ability, t.series_name
        FROM treasure t
        JOIN grade g ON t.grade_code = g.grade_code
        WHERE t.treasure_id = ?
        """,
        [treasure_id]
    ).fetchone()

    if not row:
        return ft.View(
            route=f"/treasures/{treasure_id}",
            controls=[ft.Text("보물 정보를 찾을 수 없습니다.")]
        )

    _, treasure_name, image_path, grade_code, grade_name, level, cur_ability, next_ability, series_name = row

    if image_path:
        img = ft.Image(src=image_path, width=180, height=180, fit="contain")
    else:
        img = ft.Container(width=180, height=180, bgcolor="#3a3a5c", border_radius=8)

    return ft.View(
        route=f"/treasures/{treasure_id}",
        padding=0,
        controls=[
            ft.Row(
                controls=[
                    sidebar(page),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton("← 목록", on_click=lambda e: page.go("/treasures")),
                                padding=16,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        img,
                                        ft.Column(
                                            controls=[
                                                ft.Text(treasure_name, size=22, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"등급 : {grade_name}", size=14),
                                                ft.Text(f"시리즈 : {series_name or '-'}", size=14),
                                                ft.Text(f"레벨 : {level if level else '-'}", size=14),
                                                ft.Text(f"현재 능력 : {cur_ability or '-'}", size=14),
                                                ft.Text(f"다음 능력 : {next_ability or '-'}", size=14),
                                            ],
                                            spacing=8,
                                        ),
                                    ],
                                    spacing=24,
                                ),
                                padding=16,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        ],
    )