import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def treasure_list_view(page: ft.Page):

    def load_treasures(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, grade, stat, effect FROM treasure WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, grade, stat, effect FROM treasure"
            ).fetchall()
        con.close()
        return result

    def treasure_row(treasure):
        treasure_id, name, grade, stat, effect = treasure
        return ft.GestureDetector(
            on_tap=lambda e, tid=treasure_id: page.go(f"/treasures/{tid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DIAMOND, size=40),
                        ft.Text(name, width=150, size=13),
                        ft.Text(grade if grade else "-", width=100, size=13),
                        ft.Text(stat if stat else "-", width=150, size=13),
                        ft.Text(effect if effect else "-", expand=True, size=13),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=8, bottom=8, left=10, right=10),
                border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
            ),
        )

    def table_header():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("아이콘", width=50, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("보물명", width=150, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("등급", width=100, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("능력치", width=150, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("효과", expand=True, size=13, weight=ft.FontWeight.BOLD),
                ],
                spacing=10,
            ),
            padding=ft.Padding(top=8, bottom=8, left=10, right=10),
            bgcolor=ft.Colors.GREY_200,
        )

    search_field = ft.TextField(
        hint_text="🔍 보물 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    treasure_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        treasure_list.controls.clear()
        treasures = load_treasures(keyword)
        for t in treasures:
            treasure_list.controls.append(treasure_row(t))
        page.update()

    refresh_list()

    return ft.View(
        route="/treasures",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 3),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            table_header(),
                            treasure_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
