import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def topping_list_view(page: ft.Page):

    def load_toppings(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, topping_type, main_stat, sub_stat FROM topping WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, topping_type, main_stat, sub_stat FROM topping"
            ).fetchall()
        con.close()
        return result

    def topping_row(topping):
        topping_id, name, topping_type, main_stat, sub_stat = topping
        return ft.GestureDetector(
            on_tap=lambda e, tid=topping_id: page.go(f"/toppings/{tid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CIRCLE, size=40),
                        ft.Text(name, width=150, size=13),
                        ft.Text(
                            topping_type if topping_type else "-", width=120, size=13
                        ),
                        ft.Text(main_stat if main_stat else "-", width=150, size=13),
                        ft.Text(sub_stat if sub_stat else "-", expand=True, size=13),
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
                    ft.Text("토핑명", width=150, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("종류", width=120, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("메인 스탯", width=150, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "서브 스탯", expand=True, size=13, weight=ft.FontWeight.BOLD
                    ),
                ],
                spacing=10,
            ),
            padding=ft.Padding(top=8, bottom=8, left=10, right=10),
            bgcolor=ft.Colors.GREY_200,
        )

    search_field = ft.TextField(
        hint_text="🔍 토핑 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    topping_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        topping_list.controls.clear()
        toppings = load_toppings(keyword)
        for t in toppings:
            topping_list.controls.append(topping_row(t))
        page.update()

    refresh_list()

    return ft.View(
        route="/toppings",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 1),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            table_header(),
                            topping_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
