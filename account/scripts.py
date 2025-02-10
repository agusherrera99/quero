import logging
import random

from . import models


def generate_business_types() -> list:
    business_types_data = []

    # Obtén todos los tipos de negocio
    business_types = models.BusinessType.objects.all()

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

def create_default_data(apps, schema_editor):
    # Obtén los modelos de la base de datos usando apps.get_model
    BusinessType = apps.get_model('account', 'BusinessType')
    Category = apps.get_model('stock', 'Category')
    Subcategory = apps.get_model('stock', 'Subcategory')

    # Crear categorías predeterminadas si no existen
    categories_data = [
        # Generales
        ('sin categoría', 1),
        ('bebidas', 10),
        ('fiambres', 51),
        ('embutidos', 52),

        # Panadería
        ('panes', 2),
        ('facturas', 3),
        ('tortas y postres', 4),
        ('galletitas y bizcochos', 5),
        ('confitería', 6),
        ('empanadas', 7),
        ('pizzas y focaccias', 8),
        ('panes integrales y saludables', 9),

        # Qiosco/Almacén
        ('almacen', 11),
        ('golosinas', 12),
        ('galletitas', 13),
        ('limpieza', 14),
        ('perfumeria', 15),
        ('cigarrillos', 16),

        # Verdulería
        ('frutas', 17),
        ('verduras', 18),
        ('hortalizas', 19),
        ('productos animales', 20),

        # Ferretería
        ('articulos para gas y electricidad', 21),
        ('buloneria', 22),
        ('ferreteria en general', 23),
        ('herrajes y hogar', 24),
        ('herramientas', 25),
        ('herramientas electricas', 26),
        ('insecticidas y jardineria', 27),
        ('materiales electricos', 28),
        ('materiales para la construccion', 29),
        ('pintureria', 30),
        ('plomeria', 31),
        ('quimicos y limpieza', 32),
        ('adhesivos y selladores', 33),
        ('lubricantes y aceites', 34),
        ('sanitarios', 35),
        ('seguridad', 36),
        ('sogas y tejidos', 37),

        # Libreía
        ('papeleria', 38),
        ('articulos de oficina', 39),
        ('escritura', 40),
        ('medicion', 41),
        ('cuadernos', 42),
        ('carpetas', 43),
        ('arte', 44),
        ('adhesivos', 45),
        ('corte', 46),
        
        # Carnicería
        ('vacunos', 47),
        ('porcinos', 48),
        ('aves', 49),
        ('pescados y mariscos', 50),
        ('preparados', 53),
        ('congelados', 54),
        ('carbón y leña', 55),
    ]

    for name, id in categories_data:
        Category.objects.get_or_create(id=id, name=name)

    # Crear subcategorías predeterminadas si no existen
    subcategories_data = [
        # Generales
        ('sin subcategoría', 1, 'sin categoría'),
        ('bebidas calientes', 24, 'bebidas'),
        ('bebidas frías', 25, 'bebidas'),
        ('bebidas alcohólicas y energizantes', 440, 'bebidas'),

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
        ('galletas dulces', 11, 'galletitas y bizcochos'),
        ('galletas saladas', 12, 'galletitas y bizcochos'),
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

        # Qiosco/Almacén
        ('aceites', 26, 'almacen'),
        ('acetos', 27, 'almacen'),
        ('aderezos', 28, 'almacen'),
        ('arroz y legumbres', 29, 'almacen'),
        ('azúcar y edulcorantes', 30, 'almacen'),
        ('cacaos', 31, 'almacen'),
        ('caldos y sopas', 32, 'almacen'),
        ('cereales', 33, 'almacen'),
        ('dulces y mermeladas', 34, 'almacen'),
        ('encurtidos', 35, 'almacen'),
        ('enlatados', 36, 'almacen'),
        ('especias y condimentos', 37, 'almacen'),
        ('fideos y pastas', 38, 'almacen'),
        ('harinas y premezclas', 39, 'almacen'),
        ('infusiones', 40, 'almacen'),
        ('jugos', 41, 'almacen'),
        ('lacteos', 42, 'almacen'),
        ('panificados', 43, 'almacen'),
        ('snacks', 44, 'almacen'),
        ('galletitas dulces', 45, 'galletitas'),
        ('galletitas saladas', 46, 'galletitas'),
        ('galletitas sin sal', 47, 'galletitas'),
        ('barras de cereal', 48, 'golosinas'),
        ('bombones', 49, 'golosinas'),
        ('caramelos', 50, 'golosinas'),
        ('chicles', 51, 'golosinas'),
        ('chocolates', 52, 'golosinas'),
        ('chupetines', 53, 'golosinas'),
        ('gomitas', 54, 'golosinas'),
        ('pastillas', 55, 'golosinas'),
        ('turrones', 56, 'golosinas'),
        ('alchol', 57, 'limpieza'),
        ('jabones', 58, 'limpieza'),
        ('limpieza de baño', 59, 'limpieza'),
        ('limpieza de cocina', 60, 'limpieza'),
        ('limpieza del hogar', 61, 'limpieza'),
        ('limpieza de ropa', 62, 'limpieza'),
        ('alcohol', 63, 'perfumeria'),
        ('bebes', 64, 'perfumeria'),
        ('colonias y perfumes', 65, 'perfumeria'),
        ('cuidado bucal', 66, 'perfumeria'),
        ('cuidado capilar', 67, 'perfumeria'),
        ('cuidado corporal', 68, 'perfumeria'),
        ('cuidado facial', 69, 'perfumeria'),
        ('desodorantes', 70, 'perfumeria'),
        ('espumas y geles', 71, 'perfumeria'),
        ('filos', 72, 'perfumeria'),
        ('papeleria', 444, 'perfumeria'),
        ('protección femenina', 73, 'perfumeria'),
        ('protección masculina', 74, 'perfumeria'),
        ('protección solar', 75, 'perfumeria'),
        ('marlboro', 76, 'cigarrillos'),
        ('parlament', 77, 'cigarrillos'),
        ('camel', 78, 'cigarrillos'),
        ('lucky strike', 79, 'cigarrillos'),
        ('chesterfield', 80, 'cigarrillos'),
        ('dunhill', 81, 'cigarrillos'),
        ('rothmans', 82, 'cigarrillos'),
        ('philip morris', 83, 'cigarrillos'),
        ('alfajores', 443, 'golosinas'),

        # Verdulería
        ('frutas cítricas', 84, 'frutas'),
        ('frutas de carozo', 85, 'frutas'),
        ('frutas tropicales', 86, 'frutas'),
        ('frutas del bosque', 87, 'frutas'),
        ('frutas secas', 88, 'frutas'),
        ('frutas desecadas', 89, 'frutas'),
        ('verduras de hoja', 90, 'verduras'),
        ('verduras de raíz', 91, 'verduras'),
        ('verduras de bulbo', 92, 'verduras'),
        ('verduras de tallo', 93, 'verduras'),
        ('verduras de flor', 94, 'verduras'),
        ('verduras de fruto', 95, 'verduras'),
        ('verduras de semilla', 96, 'verduras'),
        ('verduras de tubérculo', 97, 'verduras'),
        ('verduras de rizoma', 98, 'verduras'),
        ('verduras de corteza', 99, 'verduras'),
        ('hortalizas de hoja', 100, 'hortalizas'),
        ('hortalizas de raíz', 101, 'hortalizas'),
        ('hortalizas de bulbo', 102, 'hortalizas'),
        ('hortalizas de tallo', 103, 'hortalizas'),
        ('hortalizas de flor', 104, 'hortalizas'),
        ('hortalizas de fruto', 105, 'hortalizas'),
        ('hortalizas de semilla', 106, 'hortalizas'),
        ('hortalizas de tubérculo', 107, 'hortalizas'),
        ('hortalizas de rizoma', 108, 'hortalizas'),
        ('hortalizas de corteza', 109, 'hortalizas'),
        ('avicola', 110, 'productos animales'),

        # Ferretería
        ('anafes', 111, 'articulos para gas y electricidad'),
        ('calefones', 112, 'articulos para gas y electricidad'),
        ('calentadores', 113, 'articulos para gas y electricidad'),
        ('difragmas', 114, 'articulos para gas y electricidad'),
        ('estufas/caloventores', 115, 'articulos para gas y electricidad'),
        ('extractores', 116, 'articulos para gas y electricidad'),
        ('faroles a gas', 117, 'articulos para gas y electricidad'),
        ('pantallas', 118, 'articulos para gas y electricidad'),
        ('planchas', 119, 'articulos para gas y electricidad'),
        ('quemadores', 120, 'articulos para gas y electricidad'),
        ('termotanques', 121, 'articulos para gas y electricidad'),
        ('alambre', 122, 'buloneria'),
        ('alemites', 123, 'buloneria'),
        ('anillos de seguridad', 124, 'buloneria'),
        ('arandelas', 125, 'buloneria'),
        ('barras roscadas', 126, 'buloneria'),
        ('bulones', 127, 'buloneria'),
        ('brocas', 128, 'buloneria'),
        ('chavetas', 129, 'buloneria'),
        ('clavos', 130, 'buloneria'),
        ('conos', 131, 'buloneria'),
        ('contra tuercas', 132, 'buloneria'),
        ('esparragos', 133, 'buloneria'),
        ('espinas elásticas', 134, 'buloneria'),
        ('mariposas', 135, 'buloneria'),
        ('pitones', 136, 'buloneria'),
        ('remaches', 137, 'buloneria'),
        ('tacos', 138, 'buloneria'),
        ('tarugos', 139, 'buloneria'),
        ('tornillos', 140, 'buloneria'),
        ('tuercas', 143, 'buloneria'),
        ('varillas roscadas', 144, 'buloneria'),
        ('adaptadores', 145, 'ferreteria en general'),
        ('argollas', 146, 'ferreteria en general'),
        ('armarios y cajones', 147, 'ferreteria en general'),
        ('bancos de trabajo', 148, 'ferreteria en general'),
        ('cables', 149, 'ferreteria en general'),
        ('carbones', 150, 'ferreteria en general'),
        ('carretillas', 151, 'ferreteria en general'),
        ('cintas aislantes', 152, 'ferreteria en general'),
        ('cintas de embalaje', 153, 'ferreteria en general'),
        ('cintas doble faz', 154, 'ferreteria en general'),
        ('cintas para demarcación', 155, 'ferreteria en general'),
        ('contenedores', 156, 'ferreteria en general'),
        ('correas', 157, 'ferreteria en general'),
        ('discos', 158, 'ferreteria en general'),
        ('electrodos', 159, 'ferreteria en general'),
        ('embudos', 160, 'ferreteria en general'),
        ('estantes', 161, 'ferreteria en general'),
        ('gaveteros', 162, 'ferreteria en general'),
        ('hilos', 163, 'ferreteria en general'),
        ('infladores', 164, 'ferreteria en general'),
        ('mechas', 165, 'ferreteria en general'),
        ('mosquetones', 166, 'ferreteria en general'),
        ('organizadores', 167, 'ferreteria en general'),
        ('tensores', 168, 'ferreteria en general'),
        ('barrales', 169, 'herrajes y hogar'),
        ('bisagras', 170, 'herrajes y hogar'),
        ('botiquines', 171, 'herrajes y hogar'),
        ('burletes', 172, 'herrajes y hogar'),
        ('cadenas', 173, 'herrajes y hogar'),
        ('cerraduras', 174, 'herrajes y hogar'),
        ('candados', 175, 'herrajes y hogar'),
        ('caños', 176, 'herrajes y hogar'),
        ('cobertores', 177, 'herrajes y hogar'),
        ('escuadras', 178, 'herrajes y hogar'),
        ('eslingas', 179, 'herrajes y hogar'),
        ('filtro de agua', 180, 'herrajes y hogar'),
        ('ganchos', 181, 'herrajes y hogar'),
        ('limpieza de hogar', 182, 'herrajes y hogar'),
        ('manijas', 183, 'herrajes y hogar'),
        ('pasadores', 184, 'herrajes y hogar'),
        ('perchas', 185, 'herrajes y hogar'),
        ('soportes para aire acondicionado', 186, 'herrajes y hogar'),
        ('soportes para tv', 187, 'herrajes y hogar'),
        ('soportes para ventiladores', 188, 'herrajes y hogar'),
        ('soportes para espejos', 189, 'herrajes y hogar'),
        ('soportes para estantes', 190, 'herrajes y hogar'),
        ('termos', 191, 'herrajes y hogar'),
        ('utensilios de cocina', 192, 'herrajes y hogar'),
        ('zócalos', 193, 'herrajes y hogar'),
        ('alicates', 194, 'herramientas'),
        ('azadas', 195, 'herramientas'),
        ('baldes', 196, 'herramientas'),
        ('barrenos', 197, 'herramientas'),
        ('barretas', 198, 'herramientas'),
        ('bocallaves', 199, 'herramientas'),
        ('bolsos', 200, 'herramientas'),
        ('calibres', 201, 'herramientas'),
        ('cepillos', 202, 'herramientas'),
        ('cinceles', 203, 'herramientas'),
        ('cintas metricas', 204, 'herramientas'),
        ('corta vidrios', 205, 'herramientas'),
        ('cortadoras', 206, 'herramientas'),
        ('cortafierros', 207, 'herramientas'),
        ('cortatubos', 208, 'herramientas'),
        ('criquets', 209, 'herramientas'),
        ('cucharas', 210, 'herramientas'),
        ('cutters y cuchillas', 211, 'herramientas'),
        ('destornilladores', 212, 'herramientas'),
        ('engrapadoras', 213, 'herramientas'),
        ('fratachos', 214, 'herramientas'),
        ('hojas de sierra', 215, 'herramientas'),
        ('hormigoneras', 216, 'herramientas'),
        ('horquillas', 217, 'herramientas'),
        ('lijas', 218, 'herramientas'),
        ('limas', 219, 'herramientas'),
        ('llaves', 220, 'herramientas'),
        ('mandriles', 221, 'herramientas'),
        ('martillos', 222, 'herramientas'),
        ('mazas', 223, 'herramientas'),
        ('morsas', 224, 'herramientas'),
        ('palas', 225, 'herramientas'),
        ('picos', 226, 'herramientas'),
        ('pela cables', 227, 'herramientas'),
        ('pinzas', 228, 'herramientas'),
        ('pistolas de calor', 229, 'herramientas'),
        ('pistolas de silicona', 230, 'herramientas'),
        ('amoladoras', 231, 'herramientas electricas'),
        ('aspiradoras', 232, 'herramientas electricas'),
        ('sopladoras', 233, 'herramientas electricas'),
        ('baterias', 234, 'herramientas electricas'),
        ('bombas de agua', 235, 'herramientas electricas'),
        ('bordeadoras', 236, 'herramientas electricas'),
        ('cargadores', 237, 'herramientas electricas'),
        ('cepilladoras', 238, 'herramientas electricas'),
        ('clavadoras', 239, 'herramientas electricas'),
        ('compresores', 240, 'herramientas electricas'),
        ('cortadoras de plasma', 241, 'herramientas electricas'),
        ('grabadoras electricas', 242, 'herramientas electricas'),
        ('hidrolavadoras', 243, 'herramientas electricas'),
        ('lijadoras', 244, 'herramientas electricas'),
        ('llaves de impacto', 245, 'herramientas electricas'),
        ('lustralijadoras', 246, 'herramientas electricas'),
        ('martillos demoledores', 247, 'herramientas electricas'),
        ('martillos perforadores', 248, 'herramientas electricas'),
        ('oscilatorias', 249, 'herramientas electricas'),
        ('perforadoras', 250, 'herramientas electricas'),
        ('rebajadoras', 251, 'herramientas electricas'),
        ('rotomartillos', 252, 'herramientas electricas'),
        ('sierras electricas', 253, 'herramientas electricas'),
        ('soldadoras', 254, 'herramientas electricas'),
        ('taladros', 255, 'herramientas electricas'),
        ('tornos', 256, 'herramientas electricas'),
        ('accesorios de jardineria', 257, 'insecticidas y jardineria'),
        ('barrehojas', 258, 'insecticidas y jardineria'),
        ('collares', 259, 'insecticidas y jardineria'),
        ('flotadores', 260, 'insecticidas y jardineria'),
        ('hachas', 261, 'insecticidas y jardineria'),
        ('limpiapiletas', 262, 'insecticidas y jardineria'),
        ('mangueras', 263, 'insecticidas y jardineria'),
        ('pulverizadores', 264, 'insecticidas y jardineria'),
        ('rastrillos', 265, 'insecticidas y jardineria'),
        ('rociadores', 266, 'insecticidas y jardineria'),
        ('venenos', 267, 'insecticidas y jardineria'),
        ('alargues', 268, 'materiales electricos'),
        ('accesorios para tv', 269, 'materiales electricos'),
        ('bases', 270, 'materiales electricos'),
        ('cables', 271, 'materiales electricos'),
        ('caños corrugados', 272, 'materiales electricos'),
        ('caños rígidos', 273, 'materiales electricos'),
        ('cintas aislantes', 274, 'materiales electricos'),
        ('diyuntores/diferenciasles', 275, 'materiales electricos'),
        ('fichas', 276, 'materiales electricos'),
        ('lamparas', 277, 'materiales electricos'),
        ('modulos', 278, 'materiales electricos'),
        ('porta lamparas', 279, 'materiales electricos'),
        ('precintos', 280, 'materiales electricos'),
        ('prolongadores', 281, 'materiales electricos'),
        ('sensores', 282, 'materiales electricos'),
        ('tapas de luz', 283, 'materiales electricos'),
        ('termicas', 284, 'materiales electricos'),
        ('timbres', 285, 'materiales electricos'),
        ('veladores', 286, 'materiales electricos'),
        ('zapatillas', 287, 'materiales electricos'),
        ('adhesivos', 288, 'material para la construccion'),
        ('arenas', 289, 'material para la construccion'),
        ('cementos', 290, 'material para la construccion'),
        ('cintas', 291, 'material para la construccion'),
        ('hidrofugos', 292, 'material para la construccion'),
        ('mezclas', 293, 'material para la construccion'),
        ('pegamentos', 294, 'material para la construccion'),
        ('aerografos', 295, 'pintureria'),
        ('aerosoles', 296, 'pintureria'),
        ('bandejas', 297, 'pintureria'),
        ('barnices', 298, 'pintureria'),
        ('brochas', 299, 'pintureria'),
        ('caballetes', 300, 'pintureria'),
        ('diluyentes', 301, 'pintureria'),
        ('espatulas', 302, 'pintureria'),
        ('enduidos', 303, 'pintureria'),
        ('esmaltes', 304, 'pintureria'),
        ('esponjas', 305, 'pintureria'),
        ('fijadores', 306, 'pintureria'),
        ('impermeabilizantes', 307, 'pintureria'),
        ('lacas', 308, 'pintureria'),
        ('látex', 309, 'pintureria'),
        ('lijas', 310, 'pintureria'),
        ('masillas', 311, 'pintureria'),
        ('pinceles', 312, 'pintureria'),
        ('membranas', 313, 'pintureria'),
        ('revestimientos', 314, 'pintureria'),
        ('rodillos', 315, 'pintureria'),
        ('selladores', 316, 'pintureria'),
        ('pinturas', 317, 'pintureria'),
        ('protectores', 318, 'pintureria'),
        ('tintas', 319, 'pintureria'),
        ('abrazaderas', 320, 'plomeria'),
        ('grampas', 321, 'plomeria'),
        ('soportes', 322, 'plomeria'),
        ('acoples', 323, 'plomeria'),
        ('adhesivos', 324, 'plomeria'),
        ('cabezales', 325, 'plomeria'),
        ('vastagos', 326, 'plomeria'),
        ('canillas', 327, 'plomeria'),
        ('caños', 328, 'plomeria'),
        ('cintas', 329, 'plomeria'),
        ('conexiones', 330, 'plomeria'),
        ('destapadores', 331, 'plomeria'),
        ('espigas', 332, 'plomeria'),
        ('flexibles', 333, 'plomeria'),
        ('flotantes', 334, 'plomeria'),
        ('griferias', 335, 'plomeria'),
        ('mangueras', 336, 'plomeria'),
        ('sifones', 337, 'plomeria'),
        ('tuberias', 338, 'plomeria'),
        ('termocuplas', 339, 'plomeria'),
        ('valvulas', 340, 'plomeria'),
        ('adhesivos', 341, 'quimicos y limpieza'),
        ('alcohol', 342, 'quimicos y limpieza'),
        ('antigrasas', 343, 'quimicos y limpieza'),
        ('antihumedad', 344, 'quimicos y limpieza'),
        ('antioxidantes', 345, 'quimicos y limpieza'),
        ('cloros', 346, 'quimicos y limpieza'),
        ('desengrasantes', 347, 'quimicos y limpieza'),
        ('desinfectantes', 348, 'quimicos y limpieza'),
        ('detergentes', 349, 'quimicos y limpieza'),
        ('diluyentes', 350, 'quimicos y limpieza'),
        ('insecticidas', 351, 'quimicos y limpieza'),
        ('lubricantes', 352, 'quimicos y limpieza'),
        ('bachas', 353, 'sanitarios'),
        ('bañeras', 354, 'sanitarios'),
        ('bidets', 355, 'sanitarios'),
        ('inodoros', 356, 'sanitarios'),
        ('lavatorios', 357, 'sanitarios'),
        ('mingitorios', 358, 'sanitarios'),
        ('piletas', 359, 'sanitarios'),
        ('tapas', 360, 'sanitarios'),
        ('valvulas', 361, 'sanitarios'),
        ('anteojos', 362, 'seguridad'),
        ('antiparras', 363, 'seguridad'),
        ('barbijos', 364, 'seguridad'),
        ('botas', 365, 'seguridad'),
        ('cascos', 366, 'seguridad'),
        ('chalecos', 367, 'seguridad'),
        ('fajas', 368, 'seguridad'),
        ('guantes', 369, 'seguridad'),
        ('mascaras', 370, 'seguridad'),
        ('protectores auditivos', 371, 'seguridad'),
        ('protectores faciales', 372, 'seguridad'),
        ('cerramientos', 373, 'sogas y tejidos'),
        ('sogas', 374, 'sogas y tejidos'),
        ('tanza', 375, 'sogas y tejidos'),
        ('tejidos', 376, 'sogas y tejidos'),

        # Libreria
        ('resmas', 377, 'papeleria'),
        ('papel', 378, 'papeleria'),
        ('cartulinas', 379, 'papeleria'),
        ('cartones', 380, 'papeleria'),
        ('bolsas', 381, 'papeleria'),
        ('abrochadoras', 382, 'articulos de oficina'),
        ('perforadoras', 383, 'articulos de oficina'),
        ('sellos', 384, 'articulos de oficina'),
        ('broches', 385, 'articulos de oficina'),
        ('talonarios', 386, 'articulos de oficina'),
        ('pizarras', 387, 'articulos de oficina'),
        ('porta lapices', 388, 'articulos de oficina'),
        ('organizadores', 389, 'articulos de oficina'),
        ('lapices', 390, 'escritura'),
        ('biromes', 391, 'escritura'),
        ('marcadores', 392, 'escritura'),
        ('portaminas', 393, 'escritura'),
        ('resaltadores', 394, 'escritura'),
        ('correctores', 395, 'escritura'),
        ('lapiceras', 396, 'escritura'),
        ('fibras', 397, 'escritura'),
        ('gomas', 398, 'escritura'),
        ('sacapuntas', 399, 'escritura'),
        ('reglas', 400, 'medicion'),
        ('escuadras', 401, 'medicion'),
        ('compases', 402, 'medicion'),
        ('transportadores', 403, 'medicion'),
        ('plantillas', 404, 'medicion'),
        ('escolares', 405, 'cuadernos'),
        ('universitarios', 406, 'cuadernos'),
        ('anillados', 407, 'cuadernos'),
        ('cuaderillos', 408, 'cuadernos'),
        ('carpetas', 409, 'carpetas'),
        ('libretas', 410, 'carpetas'),
        ('folios', 411, 'carpetas'),
        ('block de hojas', 412, 'carpetas'),
        ('crayones', 413, 'arte'),
        ('pinceles', 414, 'arte'),
        ('acuarelas', 415, 'arte'),
        ('oleos', 416, 'arte'),
        ('tizas', 417, 'arte'),
        ('lapices de colores', 418, 'arte'),
        ('pinturas', 419, 'arte'),
        ('masillas', 420, 'arte'),
        ('cintas adhesivas', 421, 'adhesivos'),
        ('liquidos', 422, 'adhesivos'),
        ('en barra', 423, 'adhesivos'),
        ('con glitter', 424, 'adhesivos'),
        ('universales', 425, 'adhesivos'),
        ('tijeras', 426, 'corte'),
        ('cutters', 427, 'corte'),
        ('otros', 428, 'corte'),
        ('separadores', 441, 'carpetas'),
        ('archivadores', 442, 'carpetas'),

        # Carnicería
        ('carne vacuna', 429, 'vacunos'),
        ('carne porcina', 430, 'porcinos'),
        ('carne aviar', 431, 'aves'),
        ('pescados', 432, 'pescados y mariscos'),
        ('mariscos', 433, 'pescados y mariscos'),
        ('fiambres', 434, 'fiambres'),
        ('embutidos', 435, 'embutidos'),
        ('preparados', 436, 'preparados'),
        ('congelados', 437, 'congelados'),
        ('carbon', 438, 'carbón y leña'),
        ('leña', 439, 'carbón y leña'),
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
        ('quisco', 2, 'Venta de productos de consumo diario, prensa y artículos variados.', ['almacen', 'bebidas', 'golosinas', 'galletitas', 'limpieza', 'perfumeria', 'cigarrillos', 'fiambres', 'embutidos']),
        ('panadería', 3, 'Elaboración y venta de productos de panadería y pastelería frescos.', ['panes', 'facturas', 'tortas y postres', 'galletitas y bizcochos', 'confitería', 'empanadas', 'pizzas y focaccias', 'panes integrales y saludables', 'bebidas']),
        ('verdulería', 4, 'Venta de frutas y verduras frescas.', ['frutas', 'verduras', 'hortalizas', 'productos animales', 'bebidas']),
        ('ferretería', 5, 'Suministro de herramientas, materiales de construcción y artículos para el hogar.', ['articulos para gas y electricidad', 'buloneria', 'ferreteria en general', 'herrajes y hogar', 'herramientas', 'herramientas electricas', 'insecticidas y jardineria', 'materiales electricos', 'material para la construccion', 'pintureria', 'plomeria', 'quimicos y limpieza', 'sanitarios', 'seguridad', 'sogas y tejidos']),
        ('librería', 6, 'Venta de libros, materiales de oficina y artículos escolares.', ['papeleria', 'articulos de oficina', 'escritura', 'medicion', 'cuadernos', 'carpetas', 'arte', 'adhesivos', 'corte']),
        ('carnicería', 7, 'Venta de productos cárnicos frescos, embutidos y artículos variados.', ['vacunos', 'porcinos', 'aves', 'pescados y mariscos', 'fiambres', 'embutidos', 'preparados', 'congelados', 'carbón y leña', 'bebidas']),
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

def create_default_tiers(apps, schema_editor):
    TierModel = apps.get_model('account', 'TierModel')

    TIERS = [
        ('prueba gratuita', 1, 15),
        ('mensual', 2, 30),
        ('anual', 3, 365),
        ('de por vida', 4, 9999)
    ]

    for tier_name, id, duration in TIERS:
        tier, created = TierModel.objects.get_or_create(
            id=id,
            name=tier_name,
            duration=duration
        )
        logging.info(f"TierModel '{tier.name}' {'created' if created else 'retrieved'}")