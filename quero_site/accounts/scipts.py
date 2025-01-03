def create_default_data(apps, schema_editor):
    # Obtén los modelos de la base de datos usando apps.get_model
    BusinessType = apps.get_model('pages', 'BusinessType')
    Category = apps.get_model('stock', 'Category')
    Subcategory = apps.get_model('stock', 'Subcategory')
    Product = apps.get_model('stock', 'Product')


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
            print(f"Categoría '{category_name}' no encontrada.")


    # Crear Productos predeterminados si no existen
    products_data = [
        # Generales
        ('sin producto', 1, 'sin subcategoría', 'sin categoría'),
        ('expressp', 2, 'bebidas calientes', 'bebidas'),
        ('té', 3, 'bebidas calientes', 'bebidas'),
        ('mate', 4, 'bebidas calientes', 'bebidas'),
        ('cortado', 5, 'bebidas calientes', 'bebidas'),
        ('capuccino', 6, 'bebidas calientes', 'bebidas'),
        ('café con leche', 7, 'bebidas calientes', 'bebidas'),
        ('café', 8, 'bebidas calientes', 'bebidas'),
        ('té', 9, 'bebidas calientes', 'bebidas'),
        ('té negro', 10, 'bebidas calientes', 'bebidas'),
        ('té verde', 11, 'bebidas calientes', 'bebidas'),
        ('té de hierbas', 12, 'bebidas calientes', 'bebidas'),
        ('chocolates calientes', 13, 'bebidas calientes', 'bebidas'),
        ('té helado', 14, 'bebidas frías', 'bebidas'),
        ('jugos naturales', 15, 'bebidas frías', 'bebidas'),
        ('sodas y refrescos', 16, 'bebidas frías', 'bebidas'),
        # Panadería
        ('pan francés', 17, 'panes comunes', 'panes'),
        ('pan de miga', 18, 'panes comunes', 'panes'),
        ('pan de campo', 19, 'panes comunes', 'panes'),
        ('pan casero', 20, 'panes comunes', 'panes'),
        ('pan de leche', 21, 'panes comunes', 'panes'),
        ('pan lactal', 22, 'panes comunes', 'panes'),
        ('pan de manteca', 23, 'panes comunes', 'panes'),
        ('pan integral', 24, 'panes especiales', 'panes'),
        ('pan de avena', 25, 'panes especiales', 'panes'),
        ('pan multigrano', 26, 'panes especiales', 'panes'),
        ('pan de centeno', 27, 'panes especiales', 'panes'),
        ('pan de pita', 28, 'panes especiales', 'panes'),
        ('pan árabe', 29, 'panes especiales', 'panes'),
        ('pan de campo grande', 30, 'panes rústicos', 'panes'),
        ('pan de campo chico', 31, 'panes rústicos', 'panes'),
        ('pan de molde grande', 32, 'panes de molde', 'panes'),
        ('pan de molde chico', 33, 'panes de molde', 'panes'),
        ('medialunas de manteca', 34, 'facturas dulces', 'facturas'),
        ('medialunas de grasa', 35, 'facturas dulces', 'facturas'),
        ('croissants', 36, 'facturas dulces', 'facturas'),
        ('facturas de hojaldre', 37, 'facturas dulces', 'facturas'),
        ('rogel', 38, 'facturas dulces', 'facturas'),
        ('churros', 39, 'facturas dulces', 'facturas'),
        ('donas', 40, 'facturas dulces', 'facturas'),
        ('bombas de crema', 41, 'facturas dulces', 'facturas'),
        ('panes de crema pastelera', 42, 'facturas dulces', 'facturas'),
        ('panes de chocolate', 43, 'facturas dulces', 'facturas'),
        ('bañadas', 44, 'facturas dulces', 'facturas'),
        ('panes con queso y jamón', 50, 'facturas saladas', 'facturas'),
        ('torta de crema', 51, 'tortas', 'tortas y postres'),
        ('torta de chocolate', 52, 'tortas', 'tortas y postres'),
        ('torta de frutas', 53, 'tortas', 'tortas y postres'),
        ('torta de manzana', 54, 'tortas', 'tortas y postres'),
        ('torta de mousse', 55, 'tortas', 'tortas y postres'),
        ('torta de cumpleaños', 56, 'tortas', 'tortas y postres'),
        ('torta con dulce de leche', 57, 'tortas', 'tortas y postres'),
        ('torta helada', 58, 'tortas', 'tortas y postres'),
        ('pasteles de frutas', 59, 'pastelería', 'tortas y postres'),
        ('pasteles de crema', 60, 'pastelería', 'tortas y postres'),
        ('pasteles de chocolate', 61, 'pastelería', 'tortas y postres'),
        ('pasteles de nuez o almendra', 62, 'pastelería', 'tortas y postres'),
        ('pastelitos de dulce de leche', 63, 'pastelería', 'tortas y postres'),
        ('tarta de manzana', 64, 'tartas', 'tortas y postres'),
        ('tarta de durazno', 65, 'tartas', 'tortas y postres'),
        ('tarta de frambuesa', 66, 'tartas', 'tortas y postres'),
        ('tarta de membrillo', 67, 'tartas', 'tortas y postres'),
        ('tarta de limón', 68, 'tartas', 'tortas y postres'),
        ('tarta de queso', 69, 'tartas', 'tortas y postres'),
        ('tarta de crema pastelera', 70, 'tartas', 'tortas y postres'),
        ('tarta de chocolate', 71, 'tartas', 'tortas y postres'),
        ('galletitas de vainilla', 72, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas de chocolate', 73, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas de dulce de leche', 74, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas rellenas', 75, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas de avena', 76, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas de chocolate con chips', 77, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas de coco', 78, 'galletitas dulces', 'galletitas y bizcochos'),
        ('galletitas saladas', 79, 'galletitas saladas', 'galletitas y bizcochos'),
        ('crackers', 80, 'galletitas saladas', 'galletitas y bizcochos'),
        ('galletitas de queso', 81, 'galletitas saladas', 'galletitas y bizcochos'),
        ('cookies de chocolate', 82, 'cookies', 'galletitas y bizcochos'),
        ('cookies de avena y pasas', 83, 'cookies', 'galletitas y bizcochos'),
        ('cookies de maní', 84, 'cookies', 'galletitas y bizcochos'),
        ('chocotorta', 85, 'pastelería', 'tortas y postres'),
        ('cremas de repostería', 86, 'pastelería', 'tortas y postres'),
        ('bombones rellenos', 87, 'pastelería', 'tortas y postres'),
        ('rellenos de crema pastelera', 88, 'pastelería', 'tortas y postres'),
        ('tarta de crema con frutas', 89, 'pastelería', 'tortas y postres'),
        ('alfajores de dulce de leche', 90, 'bocaditos', 'confitería'),
        ('alfajores de chocolate', 91, 'bocaditos', 'confitería'),
        ('alfajores de maicena', 92, 'bocaditos', 'confitería'),
        ('bombones', 93, 'bocaditos', 'confitería'),
        ('chocobars', 94, 'bocaditos', 'confitería'),
        ('mini pasteles', 95, 'bocaditos', 'confitería'),
        ('tartaletas miniatura', 96, 'bocaditos', 'confitería'),
        ('empanada de carne', 97, 'empanadas de carne', 'empanadas'),
        ('empanada de pollo', 98, 'empanadas de pollo', 'empanadas'),
        ('empanada de verdura', 99, 'empanadas de verduras', 'empanadas'),
        ('empanada de jamón y queso', 100, 'empanadas de jamón y queso', 'empanadas'),
        ('empanada de queso', 101, 'empanadas de queso', 'empanadas'),
        ('empanada de dulce de leche', 102, 'empanadas dulces', 'empanadas'),
        ('empanada de batata', 103, 'empanadas dulces', 'empanadas'),
        ('pizza de muzzarella', 104, 'pizzas', 'pizzas y focaccias'),
        ('pizza de jamón y morrones', 105, 'pizzas', 'pizzas y focaccias'),
        ('pizza de anchoas', 106, 'pizzas', 'pizzas y focaccias'),
        ('pizza de fugazzetta', 107, 'pizzas', 'pizzas y focaccias'),
        ('pizza de tomate, albahaca y mozzarella', 108, 'pizzas', 'pizzas y focaccias'),
        ('focaccia de romero', 109, 'focaccias', 'pizzas y focaccias'),
        ('focaccia con aceitunas', 110, 'focaccias', 'pizzas y focaccias'),
        ('focaccia con tomate', 111, 'focaccias', 'pizzas y focaccias'),
        ('focaccia con cebolla', 112, 'focaccias', 'pizzas y focaccias'),
        ('pan integral', 113, 'panes saludables', 'panes integrales y saludables'),
        ('pan de avena', 114, 'panes saludables', 'panes integrales y saludables'),
        ('pan de centeno', 115, 'panes saludables', 'panes integrales y saludables'),
        ('pan sin gluten', 116, 'panes saludables', 'panes integrales y saludables'),
        ('pan sin azúcar', 117, 'panes saludables', 'panes integrales y saludables'),
        ('galletitas de avena', 118, 'panes saludables', 'panes integrales y saludables'),
        ('galletitas sin gluten', 119, 'panes saludables', 'panes integrales y saludables'),
    ]

    for name, id, subcategory_name, category_name in products_data:
        try:
            category = Category.objects.get(name=category_name)
            subcategory = Subcategory.objects.get(name=subcategory_name, category=category)
        except Category.DoesNotExist:
            print(f"Categoría '{category_name}' no encontrada.")
        except Subcategory.DoesNotExist:
            print(f"Subcategoría '{subcategory_name}' no encontrada para la categoría '{category_name}'.")

        Product.objects.get_or_create(id=id, name=name, subcategory=subcategory)



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

        print(f"BusinessType '{business_type.name}' {'created' if created else 'retrieved'}, categories set.")