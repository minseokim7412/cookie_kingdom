import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def topping_detail_view(page: ft.Page, topping_id: int):

    def load_topping():
        con = get_connection()
        result = con.execute(
            "SELECT id, name, topping_type, main_stat, sub_stat, set_effect FROM topping WHERE id = ?",
            [topping_id],
        ).fetchone()
        con.close()
        return result

    topping = load_topping()

    if not topping:
        return ft.View(
            route=f"/toppings/{topping_id}",
            controls=[ft.Text("토핑 정보를 찾을 수 없습니다.")],
        )

    t_id, name, topping_type, main_stat, sub_stat, set_effect = topping

    return ft.View(
        route=f"/toppings/{topping_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 1),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/toppings"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Icon(ft.Icons.CIRCLE, size=80),
                                        ft.Text(
                                            name, size=22, weight=ft.FontWeight.BOLD
                                        ),
                                        ft.Text(
                                            f"종류: {topping_type if topping_type else '-'}",
                                            size=14,
                                        ),
                                        ft.Text(
                                            f"메인 스탯: {main_stat if main_stat else '-'}",
                                            size=14,
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
                                            "서브 스탯",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            sub_stat if sub_stat else "서브 스탯 없음",
                                            size=13,
                                            color=ft.Colors.GREY_700,
                                        ),
                                        ft.Divider(),
                                        ft.Text(
                                            "세트 효과",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            set_effect
                                            if set_effect
                                            else "세트 효과 없음",
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
