# -*- coding: utf-8 -*-
##############################################################################
# Módulo: florafiel_mascotas
# Empresa: FloraFiel S.L.
# Autor: Luis Miguel Agra Álvarez
# Descripción: Ficha de Mascota asociada a clientes de la tienda.
#              Permite registrar datos de las mascotas de los clientes
#              (especie, peso, nacimiento) y calcula automáticamente
#              su edad y ración diaria de pienso recomendada.
##############################################################################

{
    # -----------------------------------------------------------------------
    # IDENTIFICACIÓN DEL MÓDULO
    # Nombre visible en la pantalla de Aplicaciones de Odoo.
    # -----------------------------------------------------------------------
    'name': 'FloraFiel — Fichas de Mascotas',

    # Descripción corta que aparece bajo el nombre en la tienda de apps.
    'summary': 'Gestión de fichas de mascotas asociadas a clientes de FloraFiel S.L.',

    # Descripción larga (se muestra al abrir el módulo en Aplicaciones).
    'description': """
FloraFiel — Fichas de Mascotas
==============================
Módulo personalizado para FloraFiel S.L.

Funcionalidades:
- Ficha de mascota: especie, raza, peso, tamaño y fecha de nacimiento.
- Cálculo automático de edad (en años) a partir de la fecha de nacimiento.
- Cálculo automático de ración diaria de pienso recomendada (en gramos)
  según peso y tamaño.
- Asociación Many2one con clientes reales (res.partner, customer_rank > 0).
- Vista de mascotas integrada en la ficha del cliente (pestaña "Mascotas").
    """,

    # Autor del módulo.
    'author': 'Luis Miguel Agra Álvarez',

    # Categoría técnica de Odoo. 'Services' es adecuado para módulos
    # de gestión de clientes/datos sin ser ventas puras.
    'category': 'Services',

    # Versión: sigue el patrón odoo_version.major.minor.patch
    'version': '17.0.1.0.0',

    # -----------------------------------------------------------------------
    # DEPENDENCIAS
    # Lista de módulos que deben estar instalados ANTES que éste.
    # Si Odoo carga nuestra vista de res.partner antes de que exista
    # la vista padre (base.view_partner_form), fallará con error crítico.
    #
    # - 'base': siempre necesario (contiene res.partner, ir.model, etc.)
    # - 'contacts': proporciona la vista de formulario de contactos que
    #               vamos a heredar con XPath. SIN ESTO, el módulo rompe.
    # -----------------------------------------------------------------------
    'depends': ['base', 'contacts'],

    # -----------------------------------------------------------------------
    # ARCHIVOS DE DATOS
    # Odoo los carga EN ORDEN. El orden importa:
    #  1. security.xml  → define los grupos de acceso primero
    #  2. ir.model.access.csv → asigna permisos usando esos grupos
    #  3. mascota_views.xml → vistas del nuevo modelo
    #  4. res_partner_views.xml → herencia XPath sobre la ficha de cliente
    # -----------------------------------------------------------------------
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/mascota_views.xml',
        'views/res_partner_views.xml',
    ],

    # -----------------------------------------------------------------------
    # CONFIGURACIÓN DE INSTALACIÓN
    # -----------------------------------------------------------------------

    # True → aparece como aplicación independiente en el menú principal.
    # False → aparece solo como módulo técnico/complemento.
    'application': True,

    # True → se instala automáticamente con los datos de demo de Odoo.
    'installable': True,

    # Licencia del código.
    'license': 'LGPL-3',
}
