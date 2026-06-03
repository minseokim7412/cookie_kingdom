import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def biscuit_detail_view(page: ft.Page, biscuit_id: int):

    def load_biscuit():
        con = get_connection()
        result = con.execute(
            "SELECT id, name, grade, stat, effect FROM biscuit WHERE id = ?",
            [biscuit_id],
        ).fetchone()
        con.close()
        return result

    biscuit = load_biscuit()

    if not biscuit:
        return ft.View(
            route=f"/biscuits/{biscuit_id}",
            controls=[ft.Text("비스킷 정보를 찾을 수 없습니다.")],
        )

    b_id, name, grade, stat, effect = biscuit

    return ft.View(
        route=f"/biscuits/{biscuit_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 2),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/biscuits"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.STAR, size=80),
                                        ft.Text(
                                            name, size=22, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"등급: {grade if grade else '-'}", size=14
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
                                            "능력치", size=16, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            stat if stat else "능력치 정보 없음",
                                            size=13,
                                            color=ft.Colors.GREY_700,
                                        ),
                                        ft.Divider(),
                                        ft.Text(
                                            "효과", size=16, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            effect if effect else "효과 정보 없음",
                                            size=13,
                                            color=ft.Colors.GREY_700,
                                        ),
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
