from sql.models import *
import os
import random
import glob

async def main():

    await Category.objects.create(name="Male", categorytype="Sex")
    await Category.objects.create(name="Female", categorytype="Sex")
    await Category.objects.create(name="Red", categorytype="Colour")
    await Category.objects.create(name="Black", categorytype="Colour")
    await Category.objects.create(name="Silk", categorytype="Fabric")
    await Category.objects.create(name="Cotton", categorytype="Fabric")


    cats = await Category.objects.all()
    catd = {}
    for cat in cats:
        catd.setdefault(cat.categorytype, []).append(cat)
    print(catd)

    descrip = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
    do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
    ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
    cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa
    qui officia deserunt mollit anim id est laborum"""

    images = glob.glob("static/**/*Images/*")
    images.extend(glob.glob("static/**/*.png"))

    for i in range(50):
        product = Product(name=f"Test Product {i}",
                          description=descrip,
                          price=random.randrange(1000,10000),
                          quantity=random.randrange(10,100))
        await product.upsert()
        for j in range(3):
            await ProductImage.objects.create(product=product,
                                              path=random.choice(images),
                                              sequence=j)
        cat = random.choice(catd['Sex'])
        await cat.products.add(product)
        await cat.upsert()
        for cat in catd['Colour']:
            await cat.products.add(product)
            await cat.upsert()
        for cat in catd['Fabric']:
            cat = random.choice(catd['Sex'])
            await cat.products.add(product)
            await cat.upsert()
