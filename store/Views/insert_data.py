import os
from typing import Any, Callable
from translate import Translator
from django.shortcuts import render
from store.models import Categories, Products, Brands, Descriptions, Images
import json
from EleDev.settings import MEDIA_ROOT, BASE_DIR

BASE_PATH_FOLDER = os.path.join(BASE_DIR, "store\\Каталог")


def get_product_brand(title: str) -> Any:
    """
    :param title: the name of the brand to be searched in the database
    :return: Brand returns the Brand if it exists, otherwise None
    """
    try:
        return Brands.objects.get(title=title)
    except Brands.DoesNotExist:
        return None


def insert_product(path: str, characteristic: bool) -> None:
    """
    :param characteristic:True: will return the Category and a dictionary with characteristics
                          False: None, None
    :param path: The path to the folder
    :return: (Category, Dict) or (None, None)
    (None, None) is returned in two cases:
        - if characteristic
        - is such a product already exists
    """
    number = os.path.split(path)[1]
    product = Products.objects.filter(product_code=number)

    # is such a product already exists
    if product:
        product[0].category_product.set(Categories.objects.filter(title=os.path.split(os.path.split(path)[0])[1]))
        return None
    image = number + ".jpg"
    description = number + "_description.txt"

    # get data
    with open(os.path.join(path, description), encoding='utf-8') as d_file:
        description = d_file.read()
    with open(os.path.join(path, number + "_main.json"), "r", encoding='utf-8') as j:
        main_dict = json.load(j)
    with open(os.path.join(path, number + "_characteristics.json"), "r", encoding='utf-8') as j:
        characteristic_dict = json.load(j)

    # Products
    product = Products.objects.create(title=main_dict["product_name"],
                                      brand=get_product_brand(main_dict["product_brand"]),
                                      price=0,
                                      count=0,
                                      feedback=5,
                                      product_code=int(main_dict["product_number"]),
                                      slug=int(main_dict["product_number"]),
                                      )

    product.category_product.set(Categories.objects.filter(title=os.path.split(os.path.split(path)[0])[1]))

    # Descriptions
    Descriptions.objects.create(description=description,
                                product_id=product.product_code,
                                characteristic=json.dumps(characteristic_dict, ensure_ascii=False))

    # Image
    if image in os.listdir(path):
        Images.objects.create(product_id=product.product_code,
                              image=os.path.join("product_image", image))
        os.replace(os.path.join(path, image), os.path.join(MEDIA_ROOT, os.path.join("product_image", image)))

    # Characteristic
    categories = Categories.objects.filter(title=os.path.split(os.path.split(path)[0])[1])
    result = categories[0].default_characteristic if categories[0].default_characteristic is not None else {}
    for section_key, section_value in characteristic_dict.items():
        if characteristic:
            result[section_key] = {}
        for key, item in section_value.items():
            if characteristic:
                result[section_key][key] = [item]
            else:
                try:
                    result[section_key][key].append(item) if item not in result[section_key][key] else result[section_key][key]
                except KeyError:
                    pass
    categories.update(default_characteristic=result)
    return None


def insert_brand(path: str):
    """
    :param path: The path to the folder
    :return: Brands
    """
    contents = os.listdir(path)
    info_dict = {}
    image = ""
    for content in contents:
        if ".json" in content:
            with open(os.path.join(path, content), "r", encoding='utf-8') as json_file:
                info_dict = json.load(json_file)
            continue
        if ".jpg" in content:
            image = content
    if image != "":
        os.replace(os.path.join(path, image), os.path.join(MEDIA_ROOT, os.path.join("brand_image", image)))
    obj, created = Brands.objects.get_or_create(logo=os.path.join("brand_image", image),
                                                title=info_dict["producer_title"],
                                                description=info_dict["producer_description"],
                                                slug=info_dict["producer_title"],
                                                )
    return obj


def insert_data(request):
    # store lists : [path, list folders in directory]
    unprocessed_files = [[BASE_PATH_FOLDER, os.listdir(BASE_PATH_FOLDER)]]
    i = 0
    # Are brands added
    brand = False

    # whether it is necessary to return the characteristics (works for the first product)
    characteristic = True
    while unprocessed_files:
        if i < len(unprocessed_files):
            for folder in unprocessed_files[i][1]:
                # Category image
                if ".jpg" in folder:
                    Categories.objects.filter(title=os.path.split(unprocessed_files[i][0])[1]).update(
                        image=os.path.join("categories_image", folder))
                    os.replace(os.path.join(unprocessed_files[i][0], folder),
                               os.path.join(MEDIA_ROOT, os.path.join("categories_image", folder)))
                    continue
                # Product folder
                if folder.isdigit():
                    # Before adding a product, you need to add a brand.
                    if not brand:
                        j = -2
                        while not unprocessed_files[i][1][j].isdigit():
                            insert_brand(os.path.join(unprocessed_files[i][0], unprocessed_files[i][1][j]))
                            j += -1
                        brand = True
                        continue
                    if characteristic:
                        insert_product(os.path.join(unprocessed_files[i][0], folder), characteristic=characteristic)
                        characteristic = False
                        continue
                    else:
                        insert_product(os.path.join(unprocessed_files[i][0], folder), characteristic=characteristic)
                        continue
                # add a category
                if not brand:
                    slug = folder
                    # if "," in slug:
                    #     slug = slug.replace(",", "")
                    # translator = Translator(from_lang="ru", to_lang="en")
                    # slug = translator.translate(slug)
                    # if " " in slug:
                    #     slug = slug.replace(" ", "_")
                    # if Categories.objects.filter(slug__exact=slug):
                    #     slug += "_"
                    Categories.objects.create(
                        title=folder,
                        parent_id=Categories.objects.get(title=os.path.split(unprocessed_files[i][0])[1]).id,
                        default_characteristic=None,
                        image=None,
                        slug=slug,
                    )
                    unprocessed_files.append(
                        [os.path.join(unprocessed_files[i][0], folder),
                         os.listdir(os.path.join(unprocessed_files[i][0], folder))])
            i += 1
            brand = False
            characteristic = True
        else:
            break
    return render(request, "base.html", {"result": "Adding was successful"})
