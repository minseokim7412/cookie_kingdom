import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def monster_detail_view(page: ft.Page, monster_id: int):

    def load_monster():
        con = get_connection()
        result = con.execute(
            "SELECT id, name, hp, attribute, weak_attribute FROM monster WHERE id = ?",
            [monster_id],
        ).fetchone()
        con.close()
        return result

    monster = load_monster()

    if not monster:
        return ft.View(
            route=f"/monsters/{monster_id}",
            controls=[ft.Text("몬스터 정보를 찾을 수 없습니다.")],
        )

    m_id, name, hp, attribute, weak_attribute = monster

    return ft.View(
        route=f"/monsters/{monster_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 5),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/monsters"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.BUG_REPORT, size=80),
                                        ft.Text(
                                            name, size=22, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(f"HP: {hp if hp else '-'}", size=14),
                                        ft.Text(
                                            f"속성: {attribute if attribute else '-'}",
                                            size=14,
                                        ),
                                        ft.Text(
                                            f"취약 속성: {weak_attribute if weak_attribute else '-'}",
                                            size=14,
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
