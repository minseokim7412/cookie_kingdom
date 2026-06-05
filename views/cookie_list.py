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


def cookie_list_view(page: ft.Page):
    con = get_connection()

    def load_cookies(search=""):
        return con.execute(
            "SELECT cookie_id, cookie_name, grade_code, image_path FROM cookie WHERE cookie_name LIKE ? ORDER BY grade_code, cookie_name",
            [f"%{search}%"]
        ).fetchall()

    def build_grid(rows):
        cards = []
        for row in rows:
            cookie_id, cookie_name, grade_code, image_path = row

            if image_path:
                img = ft.Image(src=image_path, width=120, height=120, fit="contain")
            else:
                img = ft.Container(width=120, height=120, bgcolor="#3a3a5c", border_radius=8)

            cards.append(
                ft.GestureDetector(
                    on_tap=lambda e, cid=cookie_id: page.go(f"/cookies/{cid}"),
                    content=ft.Column(
                        controls=[
                            img,
                            ft.Text(cookie_name, size=13, text_align=ft.TextAlign.CENTER),
                            ft.Text(grade_code, size=11, color="grey", text_align=ft.TextAlign.CENTER),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=4,
                    )
                )
            )
        return cards

    grid = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=160,
        child_aspect_ratio=0.75,
        spacing=10,
        run_spacing=10,
    )

    def refresh(search=""):
        grid.controls = build_grid(load_cookies(search))
        page.update()

    def on_search(e):
        refresh(e.control.value)

    refresh()

    return ft.View(
        route="/cookies",
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
                                        ft.TextField(hint_text="쿠키 검색", expand=True, on_change=on_search, prefix_icon=ft.Icons.SEARCH),
                                        ft.ElevatedButton("필터 ▼"),
                                    ]
                                ),
                                padding=ft.Padding(left=16, right=16, top=0, bottom=0),
                            ),
                            ft.Container(content=grid, expand=True, padding=16),
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