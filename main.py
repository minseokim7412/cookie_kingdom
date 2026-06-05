import flet as ft
from db.database import init_db


def main(page: ft.Page):
    page.title = "쿠키런: 킹덤 팀 설정"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0

    init_db()

    def route_change(e):
        page.views.clear()
        route = page.route

        if route == "/" or route == "/cookies":
            from views.cookie_list import cookie_list_view
            page.views.append(cookie_list_view(page))

        elif route.startswith("/cookies/"):
            cookie_id = int(route.split("/")[-1])
            from views.cookie_detail import cookie_detail_view
            page.views.append(cookie_detail_view(page, cookie_id))

        elif route == "/toppings":
            from views.topping_list import topping_list_view
            page.views.append(topping_list_view(page))

        elif route.startswith("/toppings/"):
            topping_id = int(route.split("/")[-1])
            from views.topping_detail import topping_detail_view
            page.views.append(topping_detail_view(page, topping_id))

        elif route == "/biscuits":
            from views.biscuit_list import biscuit_list_view
            page.views.append(biscuit_list_view(page))

        elif route.startswith("/biscuits/"):
            biscuit_id = int(route.split("/")[-1])
            from views.biscuit_detail import biscuit_detail_view
            page.views.append(biscuit_detail_view(page, biscuit_id))

        elif route == "/treasures":
            from views.treasure_list import treasure_list_view
            page.views.append(treasure_list_view(page))

        elif route.startswith("/treasures/"):
            treasure_id = int(route.split("/")[-1])
            from views.treasure_detail import treasure_detail_view
            page.views.append(treasure_detail_view(page, treasure_id))

        elif route == "/contents":
            from views.content_list import content_list_view
            page.views.append(content_list_view(page))

        elif route == "/monsters":
            from views.monster_list import monster_list_view
            page.views.append(monster_list_view(page))

        elif route == "/arena":
            from views.arena_list import arena_list_view
            page.views.append(arena_list_view(page))

        elif route == "/team":
            from views.team_build import team_build_view
            page.views.append(team_build_view(page))

        elif route == "/team/save":
            from views.team_save import team_save_view
            page.views.append(team_save_view(page))

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/cookies")


ft.app(main, assets_dir="assets")