import random
from account.models import BusinessType

def generate_business_types() -> list:
    business_types_data = []

    # Obtén todos los tipos de negocio
    business_types = BusinessType.objects.all()

    for business_type in business_types:
        if business_type.name == 'sin tipo':
            continue
        
        business_type_dict = {
            'type': business_type.name,
            'description': business_type.description if business_type.description else '',
            'categories': [],
            'subcategories': []
        }

        # Obtener las categorías asociadas a este tipo de negocio
        categories = list(business_type.category_list.all())  # Convertimos a lista para usar random.sample()

        # Seleccionar hasta 4 categorías al azar, sin duplicados
        random_categories = random.sample(categories, min(4, len(categories)))

        for category in random_categories:
            # Añadir la categoría seleccionada al diccionario
            business_type_dict['categories'].append(category.name)

            # Obtener las subcategorías asociadas a esta categoría
            subcategories = list(category.subcategory_set.all())  # Convertimos a lista

            # Seleccionar una subcategoría al azar si existen subcategorías
            if subcategories:
                random_subcategory = random.choice(subcategories)
                business_type_dict['subcategories'].append(random_subcategory.name)

        # Añadir el diccionario del tipo de negocio a la lista de datos
        business_types_data.append(business_type_dict)

    return business_types_data