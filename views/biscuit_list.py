import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def biscuit_list_view(page: ft.Page):

    def load_biscuits(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, grade, stat, effect FROM biscuit WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, grade, stat, effect FROM biscuit"
            ).fetchall()
        con.close()
        return result

    def biscuit_row(biscuit):
        biscuit_id, name, grade, stat, effect = biscuit
        return ft.GestureDetector(
            on_tap=lambda e, bid=biscuit_id: page.go(f"/biscuits/{bid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STAR, size=40),
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
                    ft.Text("비스킷명", width=150, size=13, weight=ft.FontWeight.BOLD),
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
        hint_text="🔍 비스킷 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    biscuit_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        biscuit_list.controls.clear()
        biscuits = load_biscuits(keyword)
        for b in biscuits:
            biscuit_list.controls.append(biscuit_row(b))
        page.update()

    refresh_list()

    return ft.View(
        route="/biscuits",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 2),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            table_header(),
                            biscuit_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
