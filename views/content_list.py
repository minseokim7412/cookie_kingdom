import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def content_list_view(page: ft.Page):

    def load_contents(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, content_type FROM content WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, content_type FROM content"
            ).fetchall()
        con.close()
        return result

    def content_row(content):
        content_id, name, content_type = content
        return ft.GestureDetector(
            on_tap=lambda e, cid=content_id: page.go(f"/contents/{cid}"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.SPORTS_ESPORTS, size=40, color=ft.Colors.BLUE_400
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(name, size=15, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f"종류: {'몬스터형' if content_type == 'monster' else '아레나형'}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(top=12, bottom=12, left=16, right=16),
                border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
            ),
        )

    search_field = ft.TextField(
        hint_text="🔍 컨텐츠 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    content_list = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)

    def refresh_list(keyword=""):
        content_list.controls.clear()
        contents = load_contents(keyword)
        for c in contents:
            content_list.controls.append(content_row(c))
        page.update()

    refresh_list()

    return ft.View(
        route="/contents",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 4),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            content_list,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
