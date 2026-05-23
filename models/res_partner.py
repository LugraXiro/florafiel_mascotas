# -*- coding: utf-8 -*-
##############################################################################
# Herencia Python: extension del modelo nativo res.partner
# Descripcion: Anade el campo inverso mascota_ids (One2many) al modelo
#              de contactos de Odoo, para ver las mascotas de un cliente
#              directamente desde su ficha.
##############################################################################

from odoo import models, fields


class ResPartnerMascota(models.Model):
    """
    Extiende el modelo nativo res.partner (Contactos) para anadir
    la relacion inversa con las mascotas.

    IMPORTANTE: usamos _inherit sin _name.
    - Con _name: creariamos una tabla nueva en PostgreSQL.
    - Sin _name (solo _inherit): injectamos campos en la tabla existente
      res_partner, sin tocar el codigo original de Odoo.

    Es como heredar de una clase en Python estandar, pero en lugar de
    crear un objeto nuevo, modificamos el comportamiento del original.
    """

    # ------------------------------------------------------------------
    # HERENCIA
    # Le decimos a Odoo que queremos extender res.partner, no crear
    # un modelo nuevo.
    # ------------------------------------------------------------------
    _inherit = 'res.partner'

    # ------------------------------------------------------------------
    # CAMPO ONE2MANY (relacion inversa)
    #
    # Este campo NO crea ninguna columna en la tabla res_partner.
    # Es una consulta virtual: cuando Odoo necesita saber las mascotas
    # de un cliente, ejecuta internamente algo equivalente a:
    #   SELECT * FROM florafiel_mascotas_mascota WHERE cliente_id = <mi id>
    #
    # Sintaxis: fields.One2many(
    #     'modelo.destino',   -> donde buscar
    #     'campo_inverso',    -> el Many2one en ese modelo que apunta a mi
    #     string="Etiqueta"
    # )
    # ------------------------------------------------------------------
    mascota_ids = fields.One2many(
        comodel_name='florafiel_mascotas.mascota',
        inverse_name='cliente_id',
        string='Mascotas',
        help='Mascotas registradas para este cliente en FloraFiel S.L.'
    )
