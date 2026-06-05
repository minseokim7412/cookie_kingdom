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


def biscuit_detail_view(page: ft.Page, biscuit_id: int):
    con = get_connection()

    row = con.execute(
        """
        SELECT b.biscuit_id, b.biscuit_name, b.image_path,
               b.grade_code, g.grade_name,
               b.level, b.atk, b.hp, b.extra_stat
        FROM biscuit b
        JOIN grade g ON b.grade_code = g.grade_code
        WHERE b.biscuit_id = ?
        """,
        [biscuit_id]
    ).fetchone()

    if not row:
        return ft.View(
            route=f"/biscuits/{biscuit_id}",
            controls=[ft.Text("비스킷 정보를 찾을 수 없습니다.")]
        )

    _, biscuit_name, image_path, grade_code, grade_name, level, atk, hp, extra_stat = row

    if image_path:
        img = ft.Image(src=image_path, width=180, height=180, fit="contain")
    else:
        img = ft.Container(width=180, height=180, bgcolor="#3a3a5c", border_radius=8)

    return ft.View(
        route=f"/biscuits/{biscuit_id}",
        padding=0,
        controls=[
            ft.Row(
                controls=[
                    sidebar(page),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton("← 목록", on_click=lambda e: page.go("/biscuits")),
                                padding=16,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        img,
                                        ft.Column(
                                            controls=[
                                                ft.Text(biscuit_name, size=22, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"등급 : {grade_name}", size=14),
                                                ft.Text(f"레벨 : {level if level else '-'}", size=14),
                                                ft.Text(f"공격력 : {atk if atk else '-'}", size=14),
                                                ft.Text(f"체력 : {hp if hp else '-'}", size=14),
                                                ft.Text(f"추가 능력치 : {extra_stat if extra_stat else '-'}", size=14),
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