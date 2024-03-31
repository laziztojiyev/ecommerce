from random import randint, choice

from celery import shared_task

from apps.models import Product


@shared_task
def update_name(product_id, name):
    w = Product.objects.get(id=product_id)


# def add_datas():
#     categories = Category.objects.all()
#     products = []
#     for i in range(1, 100):
#         description = f'description-{i}'
#         price = randint(1, 10) * 10
#         shipping_cost = randint(1, 10)
#         name = f'name-{i}'
#         discount = randint(1, 10) * 10
#         category = choice(categories)
#         spesification = {"rangi": f"{i}"}
#         quantity = randint(1, 100)
#
#         products.append(Product(Description=description,
#                                 price=price, shipping_cost=shipping_cost,
#                                 name=name, discount=discount, category=category, characteristics=spesification,
#                                 quantity=quantity))
#     Product.objects.bulk_create(products)



