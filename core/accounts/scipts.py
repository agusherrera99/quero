import logging


def create_default_data(apps, schema_editor):
    # Obtén los modelos de la base de datos usando apps.get_model
    BusinessType = apps.get_model('pages', 'BusinessType')
    Category = apps.get_model('stock', 'Category')
    Subcategory = apps.get_model('stock', 'Subcategory')

    # Crear categorías predeterminadas si no existen
    categories_data = [
        # Generales
        ('sin categoría', 1),
        ('bebidas', 10),
        # Panadería
        ('panes', 2),
        ('facturas', 3),
        ('tortas y postres', 4),
        ('galletitas y bizcochos', 5),
        ('confitería', 6),
        ('empanadas', 7),
        ('pizzas y focaccias', 8),
        ('panes integrales y saludables', 9),
    ]

    for name, id in categories_data:
        Category.objects.get_or_create(id=id, name=name)


    # Crear subcategorías predeterminadas si no existen
    subcategories_data = [
        # Generales
        ('sin subcategoría', 1, 'sin categoría'),
        ('bebidas calientes', 24, 'bebidas'),
        ('bebidas frías', 25, 'bebidas'),
        # Panadería
        ('panes comunes', 2, 'panes'),
        ('panes especiales', 3, 'panes'),
        ('panes rústicos', 4, 'panes'),
        ('panes de molde', 5, 'panes'),
        ('facturas dulces', 6, 'facturas'),
        ('facturas saladas', 7, 'facturas'),
        ('tortas', 8, 'tortas y postres'),
        ('pastelería', 9, 'tortas y postres'),
        ('tartas', 10, 'tortas y postres'),
        ('galletitas dulces', 11, 'galletitas y bizcochos'),
        ('galletitas saladas', 12, 'galletitas y bizcochos'),
        ('cookies', 13, 'galletitas y bizcochos'),
        ('bocaditos', 14, 'confitería'),
        ('empanadas de carne', 15, 'empanadas'),
        ('empanadas de pollo', 16, 'empanadas'),
        ('empanadas de verduras', 17, 'empanadas'),
        ('empanadas de jamón y queso', 18, 'empanadas'),
        ('empanadas de queso', 19, 'empanadas'),
        ('empanadas dulces', 20, 'empanadas'),
        ('pizzas', 21, 'pizzas y focaccias'),
        ('focaccias', 22, 'pizzas y focaccias'),
        ('panes saludables', 23, 'panes integrales y saludables'),
    ]
    
    for name, id, category_name in subcategories_data:
        # Obtener la categoría directamente en cada iteración
        try:
            category = Category.objects.get(name=category_name)
            Subcategory.objects.get_or_create(id=id, name=name, category=category)
        except Category.DoesNotExist:
            logging.info(f"Categoría '{category_name}' no encontrada.")

    # Crear BusinessType predeterminados si no existen
    business_types_data = [
        ('sin tipo', 1, 'sin descripción', ['sin categoría']),
        ('quisco', 2, 'Venta de productos de consumo diario, prensa y artículos variados.', ['sin categoría']),
        ('panadería', 3, 'Elaboración y venta de productos de panadería y pastelería frescos.', ['panes', 'facturas', 'tortas y postres', 'galletitas y bizcochos', 'confitería', 'empanadas', 'pizzas y focaccias', 'panes integrales y saludables']),
        ('verdulería', 4, 'Venta de frutas y verduras frescas.', ['sin categoría']),
        ('ferretería', 5, 'Suministro de herramientas, materiales de construcción y artículos para el hogar.', ['sin categoría']),
        ('librería', 6, 'Venta de libros, materiales de oficina y artículos escolares.', ['sin categoría']),
        ('carnicería', 7, 'Venta de productos cárnicos frescos, embutidos y artículos variados.', ['sin categoría']),
    ]

    for name, id, description, category_names in business_types_data:
        # Obtener las categorías asociadas a este tipo de negocio
        categories = Category.objects.filter(name__in=category_names)

        # Crear o recuperar el tipo de negocio
        business_type, created = BusinessType.objects.get_or_create(
            id=id,
            name=name,
            description=description
        )

        # Asignar las categorías al ManyToManyField
        business_type.category_list.set(categories)  # Usa set para reemplazar o add si quieres agregar sin eliminar

        logging.info(f"BusinessType '{business_type.name}' {'created' if created else 'retrieved'}, categories set.")