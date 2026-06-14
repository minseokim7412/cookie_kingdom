import flet as ft
from db.database import init_db


def main(page: ft.Page):
    """앱 진입점 함수 - 라우팅 및 페이지 설정"""
    page.title = "쿠키런: 킹덤 팀 설정"
    page.window.width = 1000
    page.window.height = 700
    page.padding = 0

    # DB 초기화 (테이블 생성 및 샘플 데이터 삽입)
    init_db()

    def route_change(e):
        """라우트 변경 시 해당 화면으로 전환하는 함수"""
        page.views.clear()
        route = page.route

        # 쿠키 목록 화면
        if route == "/" or route == "/cookies":
            from views.cookie_list import cookie_list_view
            page.views.append(cookie_list_view(page))

        # 쿠키 상세 화면 - URL에서 cookie_id 추출
        elif route.startswith("/cookies/"):
            cookie_id = int(route.split("/")[-1])
            from views.cookie_detail import cookie_detail_view
            page.views.append(cookie_detail_view(page, cookie_id))

        # 타르트 목록 화면
        elif route == "/toppings":
            from views.topping_list import topping_list_view
            page.views.append(topping_list_view(page))

        # 비스킷 목록 화면
        elif route == "/biscuits":
            from views.biscuit_list import biscuit_list_view
            page.views.append(biscuit_list_view(page))

        # 보물 목록 화면
        elif route == "/treasures":
            from views.treasure_list import treasure_list_view
            page.views.append(treasure_list_view(page))

        # 컨텐츠 목록 화면
        elif route == "/contents":
            from views.content_list import content_list_view
            page.views.append(content_list_view(page))

        # 몬스터 목록 화면
        elif route == "/monsters":
            from views.monster_list import monster_list_view
            page.views.append(monster_list_view(page))

        # 아레나 방어팀 목록 화면
        elif route == "/arena":
            from views.arena_list import arena_list_view
            page.views.append(arena_list_view(page))

        # 팀 편성 화면
        elif route == "/team":
            from views.team_build import team_build_view
            page.views.append(team_build_view(page))

        # 저장된 팀 편성 화면
        elif route == "/team/save":
            from views.team_save import team_save_view
            page.views.append(team_save_view(page))

        page.update()

    def view_pop(e):
        """뒤로가기 처리 함수"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # 라우트 변경 및 뒤로가기 이벤트 핸들러 등록
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # 앱 시작 시 쿠키 목록 화면으로 이동
    page.go("/cookies")


ft.app(main, assets_dir="assets")