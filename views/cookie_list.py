import flet as ft
from db.database import get_connection


def sidebar(page, selected):
    return ft.NavigationRail(
        selected_index=selected,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.FACE, label="쿠키"),
            ft.NavigationRailDestination(icon=ft.Icons.CIRCLE, label="토핑"),
            ft.NavigationRailDestination(icon=ft.Icons.STAR, label="비스킷"),
            ft.NavigationRailDestination(icon=ft.Icons.DIAMOND, label="보물"),
            ft.NavigationRailDestination(icon=ft.Icons.SPORTS_ESPORTS, label="컨텐츠"),
            ft.NavigationRailDestination(icon=ft.Icons.BUG_REPORT, label="몬스터"),
            ft.NavigationRailDestination(icon=ft.Icons.SECURITY, label="아레나"),
            ft.NavigationRailDestination(icon=ft.Icons.GROUP, label="팀 편성"),
        ],
        on_change=lambda e: page.go(
            [
                "/cookies",
                "/toppings",
                "/biscuits",
                "/treasures",
                "/contents",
                "/monsters",
                "/arena",
                "/team",
            ][e.control.selected_index]
        ),
    )


def cookie_list_view(page: ft.Page):

    def load_cookies(keyword=""):
        con = get_connection()
        if keyword:
            result = con.execute(
                "SELECT id, name, grade, attribute, position FROM cookie WHERE name LIKE ?",
                [f"%{keyword}%"],
            ).fetchall()
        else:
            result = con.execute(
                "SELECT id, name, grade, attribute, position FROM cookie"
            ).fetchall()
        con.close()
        return result

    def cookie_card(cookie):
        cookie_id, name, grade, attribute, position = cookie
        return ft.GestureDetector(
            on_tap=lambda e, cid=cookie_id: page.go(f"/cookies/{cid}"),
            content=ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.FACE, size=60),
                            ft.Text(
                                name,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                f"{grade} | {attribute}",
                                size=11,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(position, size=11, color=ft.Colors.GREY_600),
                        ],
                    ),
                )
            ),
        )

    search_field = ft.TextField(
        hint_text="🔍 쿠키 검색...",
        expand=True,
        on_submit=lambda e: refresh_list(e.control.value),
    )

    filter_btn = ft.ElevatedButton(content=ft.Text("필터 ▼"), on_click=lambda e: None)

    cookie_grid = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=160,
        child_aspect_ratio=0.75,
        spacing=10,
        run_spacing=10,
        padding=10,
    )

    def refresh_list(keyword=""):
        cookie_grid.controls.clear()
        cookies = load_cookies(keyword)
        for c in cookies:
            cookie_grid.controls.append(cookie_card(c))
        page.update()

    refresh_list()

    return ft.View(
        route="/cookies",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 0),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Row(controls=[search_field, filter_btn]),
                                padding=10,
                            ),
                            cookie_grid,
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
