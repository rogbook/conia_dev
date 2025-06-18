import time

from sqlalchemy.orm import Session

from app.database.schema import Store, CatalogStore, StoreProduct, ProductStoreMemo, StoreTheme, StoreThemeShop, StoreThemeProduct, StorePopup, StoreBoardGroup, StoreBoard, LogStore
from app.models.common import LogStoreDataIn
from app.utils.common_utils import log_msg
from scripts.database.conn import db


def make_store_theme(theme_data: StoreTheme, store_code, pid=None):
    new_theme_data = StoreTheme()
    new_theme_data.name = theme_data.name
    new_theme_data.description = theme_data.description
    new_theme_data.store_code = store_code
    if pid:
        new_theme_data.pid = pid
    new_theme_data.status = theme_data.status
    new_theme_data.layout = theme_data.layout
    new_theme_data.visible = theme_data.visible
    new_theme_data.top_visible = theme_data.top_visible
    new_theme_data.use_layout = theme_data.use_layout
    new_theme_data.sort = theme_data.sort
    return new_theme_data


def copy_theme_product_shop(session: Session, theme_id, source_theme_id):
    theme_products = sess.query(StoreThemeProduct).filter(StoreThemeProduct.store_theme_id == source_theme_id).all()
    for theme_product in theme_products:
        StoreThemeProduct.create(session=session, auto_commit=False, store_theme_id=theme_id, product_id=theme_product.product_id)

    theme_shops = sess.query(StoreThemeShop).filter(StoreThemeShop.store_theme_id == source_theme_id).all()
    for theme_shop in theme_shops:
        StoreThemeShop.create(session=session, auto_commit=False, store_theme_id=theme_id, shop_id=theme_shop.shop_id)


if __name__ == '__main__':

    db.startup()

    sess: Session
    with db.session as sess:
        copy_target_store = sess.query(Store).filter(Store.status == 'SR').all()
        for target_store in copy_target_store:
            print(f"상점 설정 복사 시작 : {target_store.title}[{target_store.code}]")
            target_store.status = 'SP'
            sess.commit()

            # 원본 상점
            source_store: Store = sess.query(Store).filter(Store.code == target_store.copy_setting).first()
            print(f"원본 상점 : {source_store.title}[{source_store.code}]")

            # 상점 기본
            target_store.type = source_store.type
            target_store.layout = source_store.layout
            target_store.auto_join = source_store.auto_join
            target_store.exclude_menu = source_store.exclude_menu
            target_store.group = source_store.group
            target_store.prd_pg_opt_use = source_store.prd_pg_opt_use
            target_store.meal_opt_use = source_store.meal_opt_use
            target_store.meal_opt_limit_use = source_store.meal_opt_limit_use
            target_store.meal_opt_limit_time = source_store.meal_opt_limit_time
            target_store.meal_opt_cancel_use = source_store.meal_opt_cancel_use
            sess.commit()
            print(f"처리 완료 - [기본 설정]")

            # 카탈로그
            sess.query(CatalogStore).filter(CatalogStore.store_code == target_store.code).delete()
            sess.commit()
            print(f"삭제 완료 - [카탈로그]")

            catalogs = sess.query(CatalogStore).filter(CatalogStore.store_code == source_store.code).all()
            for catalog in catalogs:
                CatalogStore.create(session=sess, auto_commit=False, store_code=target_store.code, catalog_id=catalog.catalog_id)
            sess.commit()
            print(f"복제 완료 - [카탈로그]")

            # 상품
            sess.query(StoreProduct).filter(StoreProduct.store_code == target_store.code).delete()
            sess.commit()
            print(f"삭제 완료 - [상품]")

            products = sess.query(StoreProduct).filter(StoreProduct.store_code == source_store.code).all()
            for product in products:
                StoreProduct.create(session=sess, auto_commit=False, product_id=product.product_id, store_code=target_store.code, catalog_id=product.catalog_id, variation=product.variation)
            sess.commit()
            print(f"복제 완료 - [상품]")

            # 상품 추가 설명
            sess.query(ProductStoreMemo).filter(ProductStoreMemo.store_code == target_store.code).delete()
            sess.commit()
            print(f"삭제 완료 - [상품 추가 설명]")

            product_memos = sess.query(ProductStoreMemo).filter(ProductStoreMemo.store_code == source_store.code).all()
            for memo in product_memos:
                ProductStoreMemo.create(session=sess, auto_commit=False, product_id=memo.product_id, store_code=target_store.code, member_id=memo.member_id, memo=memo.memo)
            sess.commit()
            print(f"복제 완료 - [상품 추가 설명]")

            # 테마
            sess.query(StoreTheme).filter(StoreTheme.store_code == target_store.code).delete()
            sess.commit()
            print(f"삭제 완료 - [테마]")

            top_themes = sess.query(StoreTheme).filter(StoreTheme.store_code == source_store.code, StoreTheme.pid == None).all()
            for top_theme in top_themes:
                new_theme = make_store_theme(top_theme, target_store.code)
                sess.add(new_theme)
                sess.flush()

                copy_theme_product_shop(sess, new_theme.id, top_theme.id)

                bottom_themes = sess.query(StoreTheme).filter(StoreTheme.store_code == source_store.code, StoreTheme.pid == top_theme.id).all()
                for bottom_theme in bottom_themes:
                    new_bottom_theme = make_store_theme(bottom_theme, target_store.code, pid=new_theme.id)
                    sess.add(new_bottom_theme)
                    sess.flush()

                    copy_theme_product_shop(sess, new_bottom_theme.id, bottom_theme.id)
            sess.commit()
            print(f"복제 완료 - [테마]")

            # 팝업
            sess.query(StorePopup).filter(StorePopup.store_code == target_store.code).delete()
            sess.commit()
            print(f"삭제 완료 - [팝업]")

            popups = sess.query(StorePopup).filter(StorePopup.store_code == source_store.code).all()
            for popup in popups:
                new_popup = StorePopup()
                new_popup.store_code = target_store.code
                new_popup.title = popup.title
                new_popup.contents = popup.contents
                new_popup.img = popup.img
                new_popup.link = popup.link
                new_popup.type = popup.type
                new_popup.status = popup.status
                new_popup.view_start_date = popup.view_start_date
                new_popup.view_end_date = popup.view_end_date
                new_popup.duplicate = popup.duplicate
                new_popup.sort = popup.sort
                sess.add(new_popup)
            sess.commit()
            print(f"복제 완료 - [팝업]")

            # 이벤트
            source_grp = sess.query(StoreBoardGroup).filter(StoreBoardGroup.store_code == source_store.code).first()
            target_grp = sess.query(StoreBoardGroup).filter(StoreBoardGroup.store_code == target_store.code).first()

            target_grp.menu_visible = source_grp.menu_visible
            target_grp.view_type = source_grp.view_type
            target_grp.view_end_content = source_grp.view_end_content

            sess.query(StoreBoard).filter(StoreBoard.store_board_group_id == target_grp.id).delete()
            sess.commit()
            print(f"삭제 완료 - [이벤트]")

            boards = sess.query(StoreBoard).filter(StoreBoard.store_board_group_id == source_grp.id).all()
            for board in boards:
                new_board = StoreBoard()
                new_board.title = board.title
                new_board.contents = board.contents
                new_board.pin = board.pin
                new_board.sort = board.sort
                new_board.status = board.status
                new_board.image = board.image
                new_board.view_start_date = board.view_start_date
                new_board.view_end_date = board.view_end_date
                new_board.start_date = board.start_date
                new_board.end_date = board.end_date
                new_board.store_board_group_id = target_grp.id
                sess.add(new_board)
            sess.commit()
            print(f"복제 완료 - [이벤트]")

            target_store.status = 'N'
            sess.commit()
            print(f"상점 설정 복사 완료 : {target_store.title}[{target_store.code}]")

            # 로깅
            log_data = LogStoreDataIn(action="수정", store_code=target_store.code, msg=log_msg("msg", f"설정 복사 완료(대상 : {source_store.title}[{source_store.code}])"), writer=f"시스템:3")
            LogStore.create(sess, auto_commit=True, **log_data.dict())

    db.shutdown()
