# -*- coding: utf-8 -*-
##############################################################################
# Modelo: florafiel_mascotas.mascota
# Descripcion: Ficha de mascota asociada a un cliente de FloraFiel S.L.
##############################################################################

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class Mascota(models.Model):
    """
    Modelo que representa la ficha de una mascota asociada a un cliente.
    Permite registrar especie, raza, peso, tamaño y fecha de nacimiento,
    y calcula automaticamente la edad y la racion diaria de pienso.
    """

    _name = 'florafiel_mascotas.mascota'
    _description = 'Ficha de Mascota — FloraFiel S.L.'
    _order = 'name asc'

    # ------------------------------------------------------------------
    # CAMPOS BASICOS
    # ------------------------------------------------------------------

    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la mascota.'
    )

    # ------------------------------------------------------------------
    # CAMPOS DE SELECCION
    # En la BD se guarda el valor tecnico (ej: 'perro'),
    # pero en pantalla se muestra la etiqueta legible (ej: 'Perro').
    # ------------------------------------------------------------------

    especie = fields.Selection(
        selection=[
            ('perro', 'Perro'),
            ('gato', 'Gato'),
            ('otro', 'Otro'),
        ],
        string='Especie',
        required=True,
        default='perro',
        help='Especie de la mascota.'
    )

    tamnho = fields.Selection(
        selection=[
            ('pqnh', 'Pequeño'),
            ('mediano', 'Mediano'),
            ('grande', 'Grande'),
        ],
        string='Tamaño',
        required=True,
        default='mediano',
        help='Tamaño de la mascota. Afecta al calculo de racion diaria.'
    )

    raza = fields.Char(
        string='Raza',
        help='Raza de la mascota (opcional).'
    )

    peso_kg = fields.Float(
        string='Peso (kg)',
        digits=(5, 2),
        help='Peso actual de la mascota en kilogramos.'
    )

    fecha_nacimiento = fields.Date(
        string='Fecha de nacimiento',
        help='Se usa para calcular la edad automaticamente.'
    )

    notas = fields.Text(
        string='Notas',
        help='Observaciones adicionales sobre la mascota.'
    )

    # ------------------------------------------------------------------
    # CAMPO RELACIONAL — Many2one a res.partner
    #
    # Many2one significa "muchas mascotas pueden pertenecer a un cliente".
    # El domain filtra para mostrar SOLO clientes reales (customer_rank > 0).
    # ------------------------------------------------------------------

    cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True,
        ondelete='cascade',
        domain=[('customer_rank', '>', 0)],
        help='Cliente propietario de la mascota. Solo se muestran clientes reales.'
    )

    # ------------------------------------------------------------------
    # CAMPOS CALCULADOS
    #
    # @api.depends: vigila los campos de origen y recalcula automaticamente.
    # store=True: guarda el resultado en BD para poder filtrar y ordenar.
    # ------------------------------------------------------------------

    edad = fields.Float(
        string='Edad (años)',
        digits=(5, 1),
        compute='_compute_edad',
        store=True,
        readonly=True,
        help='Edad calculada automaticamente desde la fecha de nacimiento.'
    )

    pienso_diario_g = fields.Integer(
        string='Ración diaria recomendada (g)',
        compute='_compute_pienso_diario',
        store=True,
        readonly=True,
        help='Ración diaria de pienso recomendada según peso, tamaño y especie.'
    )

    # ------------------------------------------------------------------
    # FUNCIONES DE CALCULO
    # ------------------------------------------------------------------

    @api.depends('fecha_nacimiento')
    def _compute_edad(self):
        """
        Calcula la edad en años con un decimal desde la fecha de nacimiento.
        Usa relativedelta para manejar correctamente años bisiestos.
        Ejemplo: 1 año y 6 meses -> 1.5
        """
        hoy = fields.Date.today()
        for record in self:
            if record.fecha_nacimiento:
                delta = relativedelta(hoy, record.fecha_nacimiento)
                record.edad = round(delta.years + delta.months / 12, 1)
            else:
                record.edad = 0.0

    @api.depends('peso_kg', 'tamnho', 'especie')
    def _compute_pienso_diario(self):
        """
        Calcula la ración diaria de pienso recomendada en gramos.

        Tabla de factores (g por kg de peso):
            Perro pequeño: 30  |  Gato pequeño: 20
            Perro mediano: 25  |  Gato mediano: 18
            Perro grande:  20  |  Gato grande:  15
            Otro (cualquier tamaño): 22
        """
        factores = {
            ('perro', 'pqnh'):    30,
            ('perro', 'mediano'): 25,
            ('perro', 'grande'):  20,
            ('gato',  'pqnh'):    20,
            ('gato',  'mediano'): 18,
            ('gato',  'grande'):  15,
        }
        for record in self:
            if record.peso_kg and record.tamnho and record.especie:
                factor = factores.get((record.especie, record.tamnho), 22)
                record.pienso_diario_g = int(record.peso_kg * factor)
            else:
                record.pienso_diario_g = 0
