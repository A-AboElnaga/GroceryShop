from product.models import Category, Brand, Product, ProductImage
from csv import reader
from django.contrib.auth.models import User
    

# name - Brand - Price - image_url
def run():
    try:
        User.objects.create_superuser(username='PeterFayez', password='f3b4a44410a4d783b4cfa65c69a41a57', email='PeterFayez@example.com')
    except:
        x = 1 
    Category.objects.all().delete()
    Brand.objects.all().delete()
    Product.objects.all().delete()
    ProductImage.objects.all().delete()
    

    
    grocery_cat = Category.objects.get_or_create(name = "grocery", slug = "grocery-1", description = "grocery items" )[0]
    
    with open("products.csv", 'r') as file:
        csvreader = reader(file, delimiter=',')
        next(csvreader)
        
        for row in csvreader:
            product_name, brand_name, price, image_url = row[0], row[1], row[3], row[4]
            price = price[4::]
            if price == '':
                price = '10'
            brand = Brand.objects.get_or_create(name = brand_name, slug = brand_name + "-1",)

            slug = ''.join(e for e in product_name if (e.isalnum() or e == ' '))
            
            product = Product.objects.get_or_create(name = product_name, 
            slug = slug.replace(' ', '_') + "-1",
            price = float(price), brand = brand[0],
            description = product_name,
            category = grocery_cat
            )
            
            image = ProductImage.objects.get_or_create(image_url=image_url, product = product[0], alt = product_name)