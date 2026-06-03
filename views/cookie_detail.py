import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def cookie_detail_view(page: ft.Page, cookie_id: int):

    def load_cookie():
        con = get_connection()
        result = con.execute(
            "SELECT id, name, grade, attribute, position, cookie_type, skill_name, skill_description FROM cookie WHERE id = ?",
            [cookie_id],
        ).fetchone()
        con.close()
        return result

    cookie = load_cookie()

    if not cookie:
        return ft.View(
            route=f"/cookies/{cookie_id}",
            controls=[ft.Text("쿠키 정보를 찾을 수 없습니다.")],
        )

    (
        c_id,
        name,
        grade,
        attribute,
        position,
        cookie_type,
        skill_name,
        skill_description,
    ) = cookie

    level_dropdown = ft.Dropdown(
        label="레벨",
        width=120,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 76)],
        value="1",
    )
    star_dropdown = ft.Dropdown(
        label="별 (승급)",
        width=120,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 6)],
        value="1",
    )
    transcendence_dropdown = ft.Dropdown(
        label="초월",
        width=120,
        options=[ft.dropdown.Option(str(i)) for i in range(0, 6)],
        value="0",
    )

    return ft.View(
        route=f"/cookies/{cookie_id}",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 0),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    content=ft.Text("← 목록"),
                                    on_click=lambda e: page.go("/cookies"),
                                ),
                                padding=10,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.FACE, size=100),
                                        ft.Column(
                                            controls=[
                                                ft.Text(
                                                    name,
                                                    size=22,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(f"등급: {grade}", size=14),
                                                ft.Text(f"속성: {attribute}", size=14),
                                                ft.Text(f"포지션: {position}", size=14),
                                                ft.Text(
                                                    f"유형: {cookie_type}", size=14
                                                ),
                                            ]
                                        ),
                                    ],
                                    spacing=20,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                                padding=20,
                            ),
                            ft.Divider(),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "레벨 / 승급 / 초월",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Row(
                                            controls=[
                                                level_dropdown,
                                                star_dropdown,
                                                transcendence_dropdown,
                                            ],
                                            spacing=20,
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
                                            "스킬 정보",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(f"스킬명: {skill_name}", size=14),
                                        ft.Text(
                                            skill_description
                                            if skill_description
                                            else "스킬 설명 없음",
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
