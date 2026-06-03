import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def content_detail_view(page: ft.Page, content_id: int):

    def load_content():
        con = get_connection()
        result = con.execute(
            "SELECT id, name, content_type FROM content WHERE id = ?", [content_id]
        ).fetchone()
        con.close()
        return result

    def load_monsters():
        con = get_connection()
        result = con.execute(
            """
            SELECT m.id, m.name, m.hp, m.attribute, m.weak_attribute
            FROM monster m
            JOIN content_monster cm ON m.id = cm.monster_id
            WHERE cm.content_id = ?
            """,
            [content_id],
        ).fetchall()
        con.close()
        return result

    content = load_content()

    if not content:
        return ft.View(
            route=f"/contents/{content_id}",
            controls=[ft.Text("컨텐츠 정보를 찾을 수 없습니다.")],
        )

    c_id, name, content_type = content

    def monster_content():
        monsters = load_monsters()
        rows = []
        for m in monsters:
            m_id, m_name, m_hp, m_attribute, m_weak = m
            rows.append(
                ft.GestureDetector(
                    on_tap=lambda e, mid=m_id: page.go(f"/monsters/{mid}"),
                    content=ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.BUG_REPORT, size=36),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            m_name, size=14, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"HP: {m_hp}  |  속성: {m_attribute}  |  취약: {m_weak}",
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.Padding(top=10, bottom=10, left=16, right=16),
                        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.GREY_300)),
                    ),
                )
            )
        return ft.Column(controls=rows, spacing=0)

    def arena_content():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "아레나 방어 팀 정보는 아레나 방어 팀 메뉴에서 확인하세요.",
                        size=13,
                        color=ft.Colors.GREY_600,
                    ),
                    ft.ElevatedButton(
                        content=ft.Text("아레나 방어 팀 보기"),
                        on_click=lambda e: page.go("/arena"),
                    ),
                ]
            ),
            padding=16,
        )

    return ft.View(
        route=f"/contents/{content_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 4),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/contents"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            name, size=22, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"종류: {'몬스터형' if content_type == 'monster' else '아레나형'}",
                                            size=14,
                                            color=ft.Colors.GREY_600,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "등장 몬스터"
                                            if content_type == "monster"
                                            else "아레나 방어 팀",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        monster_content()
                                        if content_type == "monster"
                                        else arena_content(),
                                    ]
                                ),
                                padding=20,
                            ),
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
