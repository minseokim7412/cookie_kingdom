import flet as ft
from db.database import get_connection


def sidebar(page):
    """사이드바 네비게이션 메뉴를 반환하는 함수"""
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


def content_list_view(page: ft.Page):
    """컨텐츠 목록 화면을 반환하는 함수"""
    con = get_connection()

    def load_contents(search=""):
        """검색어를 포함한 컨텐츠 목록을 DuckDB에서 조회하는 함수"""
        return con.execute(
            "SELECT content_id, content_name, content_type_name "
            "FROM content WHERE content_name LIKE ? "
            "ORDER BY content_type_name, content_name",
            [f"%{search}%"]
        ).fetchall()

    def build_table(rows):
        """컨텐츠 목록 데이터를 DataTable 행으로 변환하는 함수"""
        data_rows = []
        for row in rows:
            content_id, content_name, content_type_name = row
            data_rows.append(
                ft.DataRow(
                    cells=[
                        # 아이콘 자리 (현재 더미 박스)
                        ft.DataCell(ft.Container(width=40, height=40, bgcolor="#3a3a5c", border_radius=4)),
                        ft.DataCell(ft.Text(content_name, size=13)),
                        ft.DataCell(ft.Text(content_type_name or "-", size=13)),
                    ],
                )
            )
        return data_rows

    # 컨텐츠 목록 테이블 생성
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("아이콘")),
            ft.DataColumn(ft.Text("컨텐츠명")),
            ft.DataColumn(ft.Text("유형")),
        ],
        rows=build_table(load_contents()),
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
        """검색창 입력 시 테이블을 갱신하는 이벤트 핸들러"""
        table.rows = build_table(load_contents(e.control.value))
        page.update()

    return ft.View(
        route="/contents",
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
                                        ft.TextField(hint_text="컨텐츠 검색", expand=True, on_change=on_search, prefix_icon=ft.Icons.SEARCH),
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