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


def topping_list_view(page: ft.Page):
    con = get_connection()

    def load_tarts(search=""):
        return con.execute(
            "SELECT tart_id, tart_name, grade_code, stat, set_effect, image_path FROM tart WHERE tart_name LIKE ? ORDER BY grade_code, tart_name",
            [f"%{search}%"]
        ).fetchall()

    def build_table(rows):
        data_rows = []
        for row in rows:
            tart_id, tart_name, grade_code, stat, set_effect, image_path = row
            if image_path:
                icon = ft.Image(src=image_path, width=40, height=40, fit="contain")
            else:
                icon = ft.Container(width=40, height=40, bgcolor="#3a3a5c", border_radius=4)
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(icon),
                        ft.DataCell(ft.Text(tart_name, size=13)),
                        ft.DataCell(ft.Text(grade_code, size=13)),
                        ft.DataCell(ft.Text(str(stat) if stat else "-", size=13)),
                        ft.DataCell(ft.Text(set_effect or "-", size=13)),
                    ],
                    on_select_change=lambda e, tid=tart_id: page.go(f"/toppings/{tid}"),
                )
            )
        return data_rows

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("아이콘")),
            ft.DataColumn(ft.Text("타르트명")),
            ft.DataColumn(ft.Text("등급")),
            ft.DataColumn(ft.Text("스탯")),
            ft.DataColumn(ft.Text("세트효과")),
        ],
        rows=build_table(load_tarts()),
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
        table.rows = build_table(load_tarts(e.control.value))
        page.update()

    return ft.View(
        route="/toppings",
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
                                        ft.TextField(hint_text="타르트 검색", expand=True, on_change=on_search, prefix_icon=ft.Icons.SEARCH),
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