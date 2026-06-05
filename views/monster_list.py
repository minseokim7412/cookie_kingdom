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


def monster_list_view(page: ft.Page):
    con = get_connection()

    def load_monsters(search=""):
        return con.execute(
            "SELECT monster_id, monster_name, hp, power, atk, def FROM monster WHERE monster_name LIKE ? ORDER BY monster_name",
            [f"%{search}%"]
        ).fetchall()

    def build_table(rows):
        data_rows = []
        for row in rows:
            monster_id, monster_name, hp, power, atk, def_ = row
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(width=40, height=40, bgcolor="#3a3a5c", border_radius=4)),
                        ft.DataCell(ft.Text(monster_name, size=13)),
                        ft.DataCell(ft.Text(str(hp) if hp else "-", size=13)),
                        ft.DataCell(ft.Text(str(power) if power else "-", size=13)),
                        ft.DataCell(ft.Text(str(atk) if atk else "-", size=13)),
                        ft.DataCell(ft.Text(str(def_) if def_ else "-", size=13)),
                    ],
                )
            )
        return data_rows

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("아이콘")),
            ft.DataColumn(ft.Text("몬스터명")),
            ft.DataColumn(ft.Text("HP")),
            ft.DataColumn(ft.Text("전투력")),
            ft.DataColumn(ft.Text("공격력")),
            ft.DataColumn(ft.Text("방어력")),
        ],
        rows=build_table(load_monsters()),
        border=ft.Border(
            top=ft.BorderSide(1, "#333333"),
            bottom=ft.BorderSide(1, "#333333"),
            left=ft.BorderSide(1, "#333333"),
            right=ft.BorderSide(1, "#333333"),
        ),
        border_radius=8,
        horizontal_lines=ft.BorderSide(1, "#333333"),
    )

    def on_search(e):
        table.rows = build_table(load_monsters(e.control.value))
        page.update()

    return ft.View(
        route="/monsters",
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
                                        ft.TextField(hint_text="몬스터 검색", expand=True, on_change=on_search, prefix_icon=ft.Icons.SEARCH),
                                        ft.ElevatedButton("필터 ▼"),
                                    ]
                                ),
                                padding=ft.Padding(left=16, right=16, top=0, bottom=0),
                            ),
                            ft.Container(
                                content=ft.Column(controls=[table], scroll=ft.ScrollMode.AUTO),
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