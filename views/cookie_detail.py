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


def cookie_detail_view(page: ft.Page, cookie_id: int):
    con = get_connection()

    row = con.execute(
        """
        SELECT c.cookie_id, c.cookie_name, c.image_path,
               c.grade_code, g.grade_name,
               a.attribute_name,
               p.position_name,
               ct.cookie_type_name
        FROM cookie c
        JOIN grade g ON c.grade_code = g.grade_code
        JOIN attribute a ON c.attribute_name = a.attribute_name
        JOIN position p ON c.position_name = p.position_name
        JOIN cookie_type ct ON c.cookie_type_name = ct.cookie_type_name
        WHERE c.cookie_id = ?
        """,
        [cookie_id]
    ).fetchone()

    if not row:
        return ft.View(
            route=f"/cookies/{cookie_id}",
            controls=[ft.Text("쿠키 정보를 찾을 수 없습니다.")]
        )

    _, cookie_name, image_path, grade_code, grade_name, attribute_name, position_name, cookie_type_name = row

    if image_path:
        img = ft.Image(src=image_path, width=180, height=180, fit="contain")
    else:
        img = ft.Container(width=180, height=180, bgcolor="#3a3a5c", border_radius=8)

    return ft.View(
        route=f"/cookies/{cookie_id}",
        padding=0,
        controls=[
            ft.Row(
                controls=[
                    sidebar(page),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton("← 목록", on_click=lambda e: page.go("/cookies")),
                                padding=16,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        img,
                                        ft.Column(
                                            controls=[
                                                ft.Text(cookie_name, size=22, weight=ft.FontWeight.BOLD),
                                                ft.Text(f"등급 : {grade_name}", size=14),
                                                ft.Text(f"속성 : {attribute_name}", size=14),
                                                ft.Text(f"포지션 : {position_name}", size=14),
                                                ft.Text(f"유형 : {cookie_type_name}", size=14),
                                            ],
                                            spacing=8,
                                        ),
                                    ],
                                    spacing=24,
                                ),
                                padding=16,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("레벨 / 승급 / 초월", size=14, weight=ft.FontWeight.BOLD),
                                        ft.Row(
                                            controls=[
                                                ft.Column([ft.Text("레벨", size=12, color="grey"), ft.Text("1 ~ 100", size=13)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                                ft.Column([ft.Text("별(승급)", size=12, color="grey"), ft.Text("0 ~ 5", size=13)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                                ft.Column([ft.Text("초월", size=12, color="grey"), ft.Text("0 ~ 5", size=13)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                            ],
                                            spacing=40,
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                padding=16,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("스킬 정보", size=14, weight=ft.FontWeight.BOLD),
                                        ft.Text("스킬 설명 텍스트", size=13, color="grey"),
                                    ],
                                    spacing=8,
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