import random
from operator import itemgetter
from decimal import Decimal

from fastapi import Request
from typing import List, Dict
import json

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.common.config import conf
from app.errors import exceptions as exc
from app.utils.date_utils import D
from app.database.schema import Store, Category, ProductCategory, StoreProduct, Cart, Product, ProductOption, StoreTheme, WishProduct, StoreBoardGroup, Shop
from app.models.auth import MemberToken
from app.models.product import DataOptions, DataProduct


def get_ip(request: Request):
    """
    IP 정보
    :param request:
    :return:
    """
    if "x-forwarded-for" in request.headers.keys():
        ip = request.headers["x-forwarded-for"]
        ip = ip.split(",")[0] if "," in ip else ip
        return ip
    else:
        return request.client.host


def to_dict(model, *args, exclude: List = None):
    q_dict = {}
    for c in model.__table__.columns:
        if not args or c.name in args:
            if not exclude or c.name not in exclude:
                q_dict[c.name] = getattr(model, c.name)

    return q_dict


def list_to_dict(data_list, *args, exclude: List = None, include: List = None):
    res = []
    for row in data_list:
        q_dict = {}
        for c in row.__table__.columns:
            if not args or c.name in args:
                if not exclude or c.name not in exclude:
                    q_dict[c.name] = getattr(row, c.name)
        if include:
            for e in include:
                q_dict[e] = getattr(row, e)
        res.append(q_dict)

    return res


def make_tree(data):
    nodes = {}
    for i in data:
        idx, parent_idx = i['id'], i['pid']
        nodes[idx] = i

    forest = []
    for i in data:
        idx, parent_idx = i['id'], i['pid']
        node = nodes[idx]

        if parent_idx is None:
            parent_idx = idx

        if idx == parent_idx:
            forest.append(node)
            forest.sort(key=itemgetter('name', 'id'))
        else:
            parent = nodes.get(parent_idx, None)
            if parent:
                if 'sub' not in parent:
                    parent['sub'] = []
                sub = parent['sub']
                sub.append(node)
                sub.sort(key=itemgetter('name', 'id'))
            else:
                forest.append(node)
                forest.sort(key=itemgetter('name', 'id'))
    return forest


def order_numbering():
    now: str = D.yyyymmdd()
    rand_num: int = random.randint(0, 100000000)
    return f"{now}{str(rand_num).zfill(8)}"


def extensions_check(filename: str):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_extensions(filename: str):
    """
    파일 확장자
    :param filename:
    :return:
    """
    return filename.rsplit('.', 1)[1].lower()


def log_msg(msg_type: str, data):
    json_data = {
        "type": msg_type,
        "data": data
    }
    return json.dumps(json_data, ensure_ascii=False)


def check_store(req: Request) -> Store:
    store_code = req.path_params.get("store_code")
    if not store_code:
        raise exc.ViewNotFoundEx
    store = Store.get(code=store_code)
    if not store:
        raise exc.ViewNotFoundEx

    if store.status == 'N':
        raise exc.ViewNotFoundEx

    if store.status == 'R':
        raise exc.WaitingOpenEx
    return store


def dict_to_list(d):
    result = []
    for k, v in d.items():
        if isinstance(v, dict) and v.get("sub"):
            res = dict_to_list(v.get("sub"))
            v["sub"] = res
            result.append(v)
        else:
            result.append(v)
    return result


def make_category_tree(data: List[Category]):
    depth1 = {}

    for row in data:
        if row.depth1_id:
            if not depth1.get(row.depth1_id):
                depth1[row.depth1_id] = {
                    "id": row.depth1_id,
                    "name": row.depth1_name,
                    "sub": {},
                }

            if row.depth2_id:
                depth1_sub = depth1.get(row.depth1_id).get("sub")
                if not depth1_sub.get(row.depth2_id):
                    depth1_sub[row.depth2_id] = {
                        "id": row.depth2_id,
                        "name": row.depth2_name,
                        "sub": {},
                    }

                if row.depth3_id:
                    depth2_sub = depth1_sub.get(row.depth2_id).get("sub")
                    if not depth2_sub.get(row.depth3_id):
                        depth2_sub[row.depth3_id] = {
                            "id": row.depth3_id,
                            "name": row.depth3_name,
                            "sub": {},
                        }

                    depth3_sub = depth2_sub.get(row.depth3_id).get("sub")
                    if not depth3_sub.get(row.id):
                        depth3_sub[row.id] = {
                            "id": row.id,
                            "name": row.name,
                        }
                else:
                    depth2_sub = depth1_sub.get(row.depth2_id).get("sub")
                    if not depth2_sub.get(row.id):
                        depth2_sub[row.id] = {
                            "id": row.id,
                            "name": row.name,
                            "sub": {},
                        }
            else:
                depth1_sub = depth1.get(row.depth1_id).get("sub")
                if not depth1_sub.get(row.id):
                    depth1_sub[row.id] = {
                        "id": row.id,
                        "name": row.name,
                        "sub": {},
                    }
        else:
            if not depth1.get(row.id):
                depth1[row.id] = {
                    "id": row.id,
                    "name": row.name,
                    "sub": {},
                }

    forest = dict_to_list(depth1)
    return forest


def make_view_context_data(session: Session, req: Request, store: Store, user: MemberToken = None):
    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    category = session.query(Category) \
        .join(ProductCategory, ProductCategory.category_id == Category.id) \
        .join(StoreProduct, StoreProduct.product_id == ProductCategory.product_id) \
        .filter(StoreProduct.store_code == (dupl_target.code if dupl_target else store.code), StoreProduct.view_yn == 'Y') \
        .group_by(Category.id) \
        .all()

    category_tree = make_category_tree(category)

    cart_count = 0
    if user:
        cart_count = session.query(Cart).filter(Cart.customer_id == user.id, Cart.store_code == store.code).count()

    layout_data = None
    exclude_menu = []
    if dupl_target:
        if dupl_target.exclude_menu:
            exclude_menu = dupl_target.exclude_menu.split(',')
        if dupl_target.layout:
            layout_data = json.loads(dupl_target.layout)
    else:
        if store.exclude_menu:
            exclude_menu = store.exclude_menu.split(',')
        if store.layout:
            layout_data = json.loads(store.layout)

    themes = session.query(StoreTheme).filter(StoreTheme.store_code == (dupl_target.code if dupl_target else store.code), StoreTheme.status == 'Y', StoreTheme.visible == 'Y').order_by(StoreTheme.sort).all()
    board_grp = session.query(StoreBoardGroup).filter(StoreBoardGroup.store_code == (dupl_target.code if dupl_target else store.code)).order_by(StoreBoardGroup.sort).all()

    current_datetime = D().now
    current_time = D().now.time()

    path_count = req.url.path.count("/")

    context_data = dict(
        request=req,
        title=store.title,
        store=store,
        dupl_store=dupl_target,
        user=user,
        themes=themes,
        board_grp=board_grp,
        category=category_tree,
        layout_data=layout_data,
        api_host=conf().API_HOST,
        cart_count=cart_count,
        current_datetime=current_datetime,
        current_time=current_time,
        exclude_menu=exclude_menu,
        cookies=req.cookies,
        path_count=path_count,
    )
    return context_data


def update_product(session: Session, context_data: dict, user: MemberToken, store_code: str):
    layout_product = {}
    layout = context_data.get("layout_data")

    wish_list = []

    if context_data.get('dupl_store'):
        target_store_code = context_data['dupl_store'].code
    else:
        target_store_code = context_data['store'].code

    if layout:
        for row in layout:
            if 'column' in row['type']:
                for col in row['columns']:
                    if col['type'] == 'product':
                        prd_id = col['id']
                        store_prd = StoreProduct.get(session, product_id=prd_id, store_code=target_store_code)
                        if store_prd:
                            if user:
                                wish = WishProduct.get(session, customer_id=user.id, product_id=prd_id, store_code=store_code)
                                if wish:
                                    wish_list.append(prd_id)

                            prd = Product.get(session, id=prd_id)
                            if prd.status == 'N' or prd.view_yn == 'N':
                                continue
                            product = DataProduct.from_orm(prd)
                            variation = store_prd.variation
                            for opt in product.options:
                                if opt.default_yn == 'Y':
                                    option = DataOptions.from_orm(opt)
                                    if variation != 0:
                                        option.selling_price = option.selling_price + variation
                                    product.product_default = option
                                    break
                            check_sold_out(product)

                            layout_product[prd_id] = product
                    elif col['type'] == 'shop':
                        shop = Shop.get(session, id=col['id'])
                        if shop:
                            col['subtitle'] = shop.subtitle
                            col['badges'] = shop.badges

        context_data.update(layout_product=layout_product)
        if context_data.get('wish_list'):
            ori_wish = context_data.get('wish_list')
            ori_wish.extend(wish_list)
            context_data.update(wish_list=ori_wish)
        else:
            context_data.update(wish_list=wish_list)


def update_shop(session: Session, context_data: dict):
    layout_product = {}
    layout = context_data.get("layout_data")

    if layout:
        for row in layout:
            if 'column' in row['type']:
                for col in row['columns']:
                    if col['type'] == 'shop':
                        shop = Shop.get(session, id=col['id'])
                        if shop:
                            col['subtitle'] = shop.subtitle
                            col['badges'] = shop.badges

        context_data.update(layout_product=layout_product)


def sub_category(data, target_id):
    for item in data:
        if item['id'] == target_id:
            return item.get("sub", [])
        elif 'sub' in item:
            result = sub_category(item['sub'], target_id)
            if result is not None:
                return result
    return None


def phone_format(number):
    if number:
        if len(number) == 11:
            return '{}-{}-{}'.format(number[:3], number[3:7], number[7:])
        elif len(number) == 10:
            return '{}-{}-{}'.format(number[:3], number[3:6], number[6:])
        else:
            return number
    else:
        return number


def add_date_str(time):
    if time:
        if D().now.time() > time:
            return f"{D.tomorrow_str()} {time}"
        else:
            return f"{D.today_str()} {time}"
    else:
        return time


def qry_sorter(qry, sorter: str):
    if sorter == 'name':
        qry = qry.order_by(func.field(Product.status, 'Y', 'S', 'P', 'N'), Product.name.asc())
    elif sorter == 'newest':
        qry = qry.order_by(func.field(Product.status, 'Y', 'S', 'P', 'N'), Product.mod_date.desc())
    elif sorter == 'minPrice':
        qry = qry.order_by(func.field(Product.status, 'Y', 'S', 'P', 'N'), ProductOption.selling_price.asc())
    elif sorter == 'maxPrice':
        qry = qry.order_by(func.field(Product.status, 'Y', 'S', 'P', 'N'), ProductOption.selling_price.desc())

    return qry


def check_product_state(session, prd_id, product_option_id, store_code):
    prd = Product.get(session, id=prd_id)
    product_option = ProductOption.get(session, id=product_option_id)

    if prd.status != "Y" or prd.view_yn != "Y":
        return False

    if product_option.status != "Y" or product_option.view_yn != "Y":
        return False

    if prd.inven_use == "Y":
        if product_option.inventory.count <= product_option.inventory.safe_count:
            return False

    now = D().now
    now_time = now.time()

    if prd.sale_start_date and (prd.sale_start_date > now):
        return False

    if prd.sale_end_date and (prd.sale_end_date < now):
        return False

    if prd.sale_start_time and (prd.sale_start_time > now_time):
        return False

    if prd.sale_end_time and (prd.sale_end_time < now_time):
        return False

    store = Store.get(session, code=store_code)
    original_store = store
    dupl_target = None
    if store.dupl_store:
        dupl_target = Store.get(session, code=store.dupl_store)

    if dupl_target:
        store = dupl_target

    sp = StoreProduct.get(session, product_id=prd_id, store_code=store.code)
    if not sp:
        return False

    if sp.view_yn != "Y":
        return False

    return True


def wish_and_product_check(session, datas, user, store_code):
    wish_list = []
    products = []

    for item in datas:
        # 상품 목록에서 관심상품 표기 제거
        # if user:
        #     wish = WishProduct.get(session, customer_id=user.id, product_id=item[0].id, store_code=store_code)
        #     if wish:
        #         wish_list.append(item[0].id)

        product = DataProduct.from_orm(item[0])

        cost_variation(product, item[1])

        check_sold_out(product)

        for row in product.options:
            product.inven_cnt += (row.inventory.count - row.inventory.safe_count)

        if product.status != 'N' and product.view_yn == 'Y':
            products.append(product)

    return wish_list, products


def get_target_store_code(context_data):
    """
    복제 대상 상점 판단후 상점 코드 반환
    :param context_data:
    :return:
    """
    if context_data.get('dupl_store'):
        return context_data['dupl_store'].code
    else:
        return context_data['store'].code


def get_base_url(req: Request):
    """
    BASE URL
    :param req:
    :return:
    """
    proto = req.headers.get('X-Forwarded-Proto')
    if proto:
        return f"{proto}://{req.base_url.hostname}/"
    else:
        return req.base_url


def get_youtube_src(url: str):
    """
    유튜브 URL 에서 비디오 키 추출
    :param url:
    :return:
    """
    target_url = url.replace("http://", '').replace("https://", '')
    pattern1 = r"^(?:[\w\.]+)?youtube\.com\/watch\?v=([\w-]+)(?:&t=(\d+))?"
    pattern2 = r"^(?:[\w\.]+)?youtube\.com\/v\/([\w-]+)(?:\?t=(\d+))?"
    pattern3 = r"^(?:[\w\.]+)?youtube\.com\/embed\/([\w-]+)(?:\?start=(\d+))?"
    pattern4 = r"^(?:[\w\.]+)?youtu\.be\/([\w-]+)(?:\?t=(\d+))?"

    import re

    m1 = re.search(pattern1, target_url)
    if m1:
        return m1.group(1)

    m2 = re.search(pattern2, target_url)
    if m2:
        return m2.group(1)

    m3 = re.search(pattern3, target_url)
    if m3:
        return m3.group(1)

    m4 = re.search(pattern4, target_url)
    if m4:
        return m4.group(1)

    return url


def get_vimeo_src(url: str):
    """
    유튜브 URL 에서 비디오 키 추출
    :param url:
    :return:
    """
    target_url = url.replace("http://", '').replace("https://", '')
    pattern1 = r"^(?:[\w\.]+)?vimeo\.com\/([\w-]+)(?:&t=(\d+))?"

    import re

    m1 = re.search(pattern1, target_url)
    if m1:
        return m1.group(1)

    return url


def cost_variation(product: DataProduct, store_prd: StoreProduct):
    if store_prd and store_prd.variation != 0:
        for row in product.options:
            row.selling_price += store_prd.variation


def check_sold_out(product: DataProduct):
    is_sold_out = False
    if product.status == 'S':
        is_sold_out = True

    if product.inven_use == "Y":
        opt_cnt = len(product.options)
        sold_out_cnt = 0
        for row in product.options:
            if row.inventory.count <= row.inventory.safe_count:
                sold_out_cnt += 1
        if opt_cnt == sold_out_cnt:
            is_sold_out = True
    now = D().now
    now_time = now.time()

    if product.sale_start_date and (product.sale_start_date > now):
        product.status = 'PT'

    if product.sale_end_date and (product.sale_end_date < now):
        product.status = 'PT'

    if product.sale_start_time and (product.sale_start_time > now_time):
        product.status = 'PT'

    if product.sale_end_time and (product.sale_end_time < now_time):
        product.status = 'PT'

    if product.use_end_date and (product.use_end_date < now):
        product.status = 'PT'

    product.is_sold_out = is_sold_out


def get_user_device_type(user_agent: str):
    """
    Get device type from UserAgent
    :param user_agent:
    :return:
    """
    if user_agent:
        agent = user_agent.lower()

        if agent.find('android') > -1:
            return "MOBILE"
        elif agent.find('iphone') > -1 or agent.find('ipad') > -1 or agent.find('ipod') > -1:
            return "MOBILE"
        else:
            return "PC"
    else:
        return ""


def component_item_visible(item: Dict) -> bool:
    if item:
        if item.get('visible') is None and item.get('start_date') is None and item.get('end_date') is None:
            return True

        if item.get('visible') == 'Y':
            if item.get('start_date') or item.get('end_date'):
                if D().between_date(item.get('start_date'), item.get('end_date')):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    else:
        return False


def custom_round(num):
    if num > 0:
        if isinstance(num, Decimal):
            return int(num + Decimal(0.5))
        else:
            return int(num + 0.5)
    return int(num-0.5)


