import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def monster_list_view(page: ft.Page):

    def load_monsters(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, hp, attribute, weak_attribute FROM monster WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, hp, attribute, weak_attribute FROM monster"
            ).fetchall()
        con.close()
        return result

    def monster_row(monster):
        monster_id, name, hp, attribute, weak_attribute = monster
        return ft.GestureDetector(
            on_tap=lambda e, mid=monster_id: page.go(f"/monsters/{mid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.BUG_REPORT, size=40),
                        ft.Text(name, width=150, size=13),
                        ft.Text(str(hp) if hp else "-", width=100, size=13),
                        ft.Text(attribute if attribute else "-", width=100, size=13),
                        ft.Text(
                            weak_attribute if weak_attribute else "-",
                            expand=True,
                            size=13,
                        ),
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
                    ft.Text("몬스터명", width=150, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("HP", width=100, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text("속성", width=100, size=13, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "취약 속성", expand=True, size=13, weight=ft.FontWeight.BOLD
                    ),
                ],
                spacing=10,
            ),
            padding=ft.Padding(top=8, bottom=8, left=10, right=10),
            bgcolor=ft.Colors.GREY_200,
        )

    search_field = ft.TextField(
        hint_text="🔍 몬스터 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    monster_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        monster_list.controls.clear()
        monsters = load_monsters(keyword)
        for m in monsters:
            monster_list.controls.append(monster_row(m))
        page.update()

    refresh_list()

    return ft.View(
        route="/monsters",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 5),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            table_header(),
                            monster_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
