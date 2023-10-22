from selenium.webdriver import Chrome, Remote, ChromeOptions, ChromeService
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from database import db, engine
from models import MainLinks, ProductsFamilie, Product, Base
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

URL = 'https://web.samokat.ru/'
category_url = 'https://samokat.ru/category/'


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
browser = Remote("http://chrome:4444", DesiredCapabilities.CHROME.copy(), options=options)
# browser = Chrome()


def get_main_page_urls():
    """Поиск ссылок на главной стрвнице."""
    browser.get(URL)

    time.sleep(12)   # сон для прогрузки страницы
    main_page = browser.page_source

    soup = BeautifulSoup(main_page, 'html.parser')

    # нахождение ссылки на страничку с классными ценами
    try:
        discount_data = soup.find(
            'div', class_='DesktopShowcase_productsSlider__CE8EQ'
        )
        discount_title = discount_data.find('span').text if discount_data.find('span') else None
        list_discount_link = [
            i.get('href')
            for i in discount_data.find(
                'div', class_='ProductsPreview_root__b2_1J'
            ).children
        ]
        [_, _, discount_link] = list_discount_link
        link = URL + discount_link
        note = MainLinks(name=discount_title, link=link)
        db.add(note)
        db.commit()
    except Exception as e:
        print(f'Что-то пошло не так {e}')

    # данные с категориями товаров на странице
    data = json.loads(soup.findAll(id='__NEXT_DATA__')[0].text)

    # токен аутенофикации
    token = data['props']['pageProps']['initialState']['auth']['accessToken']

    entities = data['props']['pageProps']['initialState']['categories'][
        'catalog'
    ]['entities']

    for _, k in entities.items():
        id_ = k['id']
        name = k['name']
        rank = k['rank']
        image = k.get('image', None)
        parentId = k.get('parentId', None)
        link = (
            category_url + k.get('slug', None) if k.get('slug', None) else None
        )
        note = MainLinks(
            id_site=id_,
            name=name,
            rank=rank,
            image=image,
            parentId=parentId,
            link=link,
        )
        db.add(note)
        db.commit()


def get_data_for_categories(flag=False):
    """Обход категорий продуктов и сбор данных"""

    result = db.query(MainLinks).filter(MainLinks.link.isnot(None)).all()

    # усекание результатов для обхода по категориям
    if flag:
        result = result[:3]

    for note in result:

        browser.get(note.link)
        time.sleep(12)
        main_page = browser.page_source

        soup = BeautifulSoup(main_page, 'html.parser')

        try:
            data = json.loads(soup.findAll(id='__NEXT_DATA__')[0].text)
            entities = data['props']['pageProps']['initialState'][
                'categories'
            ]['catalog']['entities']
            for _, k in entities.items():
                id_ = k['id']
                name = k['name']
                rank = k['rank']
                productIds = k.get('productIds', None)
                parentId = k.get('parentId', None)
                link = (
                    category_url + k.get('slug', None)
                    if k.get('slug', None)
                    else None
                )

                q = db.query(ProductsFamilie).filter_by(id_site=id_).all()
                # если ключ уже существует, пропуск записи
                if q:
                    continue

                note = ProductsFamilie(
                    id_site=id_,
                    name=name,
                    rank=rank,
                    productIds=productIds,
                    parentId=parentId,
                    link=link,
                )
                db.add(note)
                db.commit()

        except Exception as e:
            print(f'Что-то пошло не так {e}')


def get_data_by_product():
    query_ = (
        db.query(ProductsFamilie)
        .filter(ProductsFamilie.productIds.isnot(None))
        .all()
    )

    for note in query_:
        list_ids = note.productIds
        for i in list_ids:
            try:
                url = 'https://samokat.ru/product/' + i

                browser.get(url)
                time.sleep(12)   # сон для прогрузки страницы
                main_page = browser.page_source

                soup = BeautifulSoup(main_page, 'html.parser')

                title = soup.find('h1', class_='_text_7xv2z_4').text
                weight = soup.find(
                    'span', class_='_text--type_h3Bold_7xv2z_32'
                ).text
                image = soup.find('img', class_='ProductImages_image__Cfpac')[
                    'src'
                ]

                # тезисное описание товара и акции
                list_abstract_description = [
                    i.text + '\n\n'
                    for i in soup.findAll(
                        'li', class_='ProductHighlights_item__k1JbP'
                    )
                ]
                abstract_description = (
                    ''.join(list_abstract_description)
                    if list_abstract_description
                    else None
                )

                # БЖУ
                nutr = (
                    soup.find(
                        'div', class_='ProductNutritions_list__pDPZB'
                    ).text
                    if soup.find('div', class_='ProductNutritions_list__pDPZB')
                    else None
                )

                # описание товара
                check_description = soup.findAll(
                    'div', class_='ProductDescription_description__RLRnL'
                )
                description = (
                    check_description[-1].text if check_description else None
                )

                # состав, сроки и условия хранения, произаодитель
                compound, shelf_life, storage_conditions, manufacturer = [
                    i.text
                    for i in soup.findAll(
                        'div', class_='AnimatedDropdownText_content__kZ_09'
                    )
                ]
                price_list = [
                    *soup.find(
                        'span', class_='_text--type_p1SemiBold_7xv2z_109'
                    ).children
                ]
                price = price_list[0].text
                if len(price_list) > 1:
                    price = price_list[0].text + '/' + price_list[1].text

                print(1, title)
                print(2, weight)
                print(3, abstract_description)
                print(4, description)
                print(5, compound)
                print(6, shelf_life)
                print(7, storage_conditions)
                print(8, manufacturer)
                print(9, price)
                print(10, nutr)
                print(11, image)
                print(12, url)
                print('Запись сделана \n\n')
                note = Product(
                    title=title,
                    weight=weight,
                    abstract_description=abstract_description,
                    description=description,
                    compound=compound,
                    shelf_life=shelf_life,
                    storage_conditions=storage_conditions,
                    manufacturer=manufacturer,
                    price=price,
                    nutr=nutr,
                    image=image,
                    link=url
                )
                db.add(note)
                db.commit()
            except Exception as e:
                print(f'Что то сломалось: {e}')


def main():
    print('START SCRIPT')

    get_main_page_urls()

    get_data_for_categories(flag=True) #  включеный флаг ограничивает выборку категорий для обхода товаров

    get_data_by_product()

    print('END SCRIPT')


if __name__ == '__main__':
    main()
