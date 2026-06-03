import flet as ft
from db.database import get_connection
from views.cookie_list import sidebar


def team_build_view(page: ft.Page):

    def load_cookies():
        con = get_connection()
        result = con.execute("SELECT id, name FROM cookie").fetchall()
        con.close()
        return result

    def load_toppings():
        con = get_connection()
        result = con.execute("SELECT id, name FROM topping").fetchall()
        con.close()
        return result

    def load_biscuits():
        con = get_connection()
        result = con.execute("SELECT id, name FROM biscuit").fetchall()
        con.close()
        return result

    def load_treasures():
        con = get_connection()
        result = con.execute("SELECT id, name FROM treasure").fetchall()
        con.close()
        return result

    def load_contents():
        con = get_connection()
        result = con.execute("SELECT id, name FROM content").fetchall()
        con.close()
        return result

    cookies = load_cookies()
    toppings = load_toppings()
    biscuits = load_biscuits()
    treasures = load_treasures()
    contents = load_contents()

    team_slots = []

    def make_slot(slot_index):
        cookie_dd = ft.Dropdown(
            label="쿠키 선택",
            width=150,
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in cookies],
        )
        topping_dd = ft.Dropdown(
            label="토핑 선택",
            width=150,
            options=[ft.dropdown.Option(str(t[0]), t[1]) for t in toppings],
        )
        biscuit_dd = ft.Dropdown(
            label="비스킷 선택",
            width=150,
            options=[ft.dropdown.Option(str(b[0]), b[1]) for b in biscuits],
        )
        level_dd = ft.Dropdown(
            label="레벨",
            width=90,
            options=[ft.dropdown.Option(str(i)) for i in range(1, 76)],
            value="1",
        )
        star_dd = ft.Dropdown(
            label="별",
            width=90,
            options=[ft.dropdown.Option(str(i)) for i in range(1, 6)],
            value="1",
        )
        transcendence_dd = ft.Dropdown(
            label="초월",
            width=90,
            options=[ft.dropdown.Option(str(i)) for i in range(0, 6)],
            value="0",
        )

        return {
            "cookie": cookie_dd,
            "topping": topping_dd,
            "biscuit": biscuit_dd,
            "level": level_dd,
            "star": star_dd,
            "transcendence": transcendence_dd,
            "widget": ft.Card(
                content=ft.Container(
                    padding=12,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                f"슬롯 {slot_index + 1}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Row(
                                controls=[
                                    cookie_dd,
                                    level_dd,
                                    star_dd,
                                    transcendence_dd,
                                ],
                                wrap=True,
                                spacing=8,
                            ),
                            ft.Row(controls=[topping_dd, biscuit_dd], spacing=8),
                        ]
                    ),
                )
            ),
        }

    for i in range(5):
        team_slots.append(make_slot(i))

    treasure_dropdowns = [
        ft.Dropdown(
            label=f"보물 {i + 1}",
            width=160,
            options=[ft.dropdown.Option(str(t[0]), t[1]) for t in treasures],
        )
        for i in range(3)
    ]

    content_dd = ft.Dropdown(
        label="컨텐츠 선택",
        width=200,
        options=[ft.dropdown.Option(str(c[0]), c[1]) for c in contents],
    )

    team_name_field = ft.TextField(label="팀 이름", width=200, hint_text="팀 이름 입력")

    save_btn = ft.ElevatedButton(
        content=ft.Text("팀 편성 저장"), on_click=lambda e: page.go("/team/save")
    )

    return ft.View(
        route="/team",
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar(page, 7),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(
                                            "팀 편성",
                                            size=22,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Divider(),
                                        ft.Text(
                                            "컨텐츠 선택",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        content_dd,
                                        ft.Divider(),
                                        ft.Text(
                                            "쿠키 편성 (최대 5명)",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Column(
                                            controls=[
                                                slot["widget"] for slot in team_slots
                                            ],
                                            spacing=10,
                                        ),
                                        ft.Divider(),
                                        ft.Text(
                                            "보물 선택 (최대 3개)",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Row(controls=treasure_dropdowns, spacing=10),
                                        ft.Divider(),
                                        ft.Row(
                                            controls=[team_name_field, save_btn],
                                            spacing=16,
                                            vertical_alignment=ft.CrossAxisAlignment.END,
                                        ),
                                    ]
                                ),
                                padding=20,
                            )
                        ],
                    ),
                ],
            )
        ],
        padding=0,
    )
