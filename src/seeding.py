from src.enum_classes import CategoryTypeEnum, SizeEnum, TagEnum, GenderEnum, ColorEnum
from sql.models import CategoryType, Category

async def seed_data():
    await seed_category_type_data()
    await seed_category_data()

async def seed_category_type_data():
    for catType in CategoryTypeEnum:
        categoryType = await CategoryType.objects.filter(CategoryType.id == catType.value).all()
        if len(categoryType) == 0:
            categoryType = CategoryType(id = catType.value, name = catType.name)
            await categoryType.save()

async def seed_category_data():
    # Seeding Size Category
    catType = await CategoryType.objects.get(CategoryType.id == CategoryTypeEnum.SIZE.value)
    for size in SizeEnum:
        category = await Category.objects.filter(Category.name == size.name).all()
        if len(category) == 0:
            category = Category(name = size.name, categorytype = catType)
            await category.save()

    # Seeding Gender Category
    catType = await CategoryType.objects.get(CategoryType.id == CategoryTypeEnum.GENDER.value)
    for gender in GenderEnum:
        category = await Category.objects.filter(Category.name == gender.name).all()
        if len(category) == 0:
            category = Category(name = gender.name, categorytype = catType)
            await category.save()

    # Seeding Tag Category
    catType = await CategoryType.objects.get(CategoryType.id == CategoryTypeEnum.TAG.value)
    for tag in TagEnum:
        category = await Category.objects.filter(Category.name == tag.name).all()
        if len(category) == 0:
            category = Category(name = tag.name, categorytype = catType)
            await category.save()


    # Seeding Color Category
    catType = await CategoryType.objects.get(CategoryType.id == CategoryTypeEnum.COLOR.value)
    for color in ColorEnum:
        category = await Category.objects.filter(Category.name == color.name).all()
        if len(category) == 0:
            category = Category(name = color.name, categorytype = catType)
            await category.save()
    
