from odoo import api, models, fields, exceptions
from dateutil.relativedelta import relativedelta



class EagleProperty(models.Model):
    _name = "eagle.property"
    _description = "Eagle Property"
    _rec_name = "name"
    _order = "construction_date DESC, id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True)
    construction_date = fields.Date(required=True, default=fields.Date.today())
    area = fields.Float(name="Area in sq. meters", compute="_compute_area")

    room_ids = fields.One2many("eagle.property.room", "property_id")
    tag_ids = fields.Many2many("eagle.tag")

    street = fields.Char(tracking=True)
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')

    # age = fields.Integer(compute="_compute_age")
    age = fields.Integer()

    parent_id = fields.Many2one("eagle.property", string="Parent Property")
    child_ids = fields.One2many("eagle.property", "parent_id", string="Child Properties")

    room_count = fields.Integer(compute="_compute_room_count")


    @api.depends("room_ids")
    def _compute_room_count(self):
        for rec in self:
            rec.room_count = len(rec.room_ids)

    @api.constrains("construction_date")
    def _contrains_construction_date(self):
        for record in self:
            if record.construction_date and record.construction_date > fields.Date.today():
                raise exceptions.ValidationError("Construction date cannot be in the future.")


    # @api.depends("construction_date")
    # def _compute_age(self):
    #     for record in self:
    #         record.age = (record.construction_date and relativedelta(fields.Date.today(), record.construction_date).years) or 0

    @api.depends("room_ids")
    def _compute_area(self):
        for rec in self:
            rec.area = sum(rec.room_ids.mapped("area"))

    _unique_name = models.Constraint("UNIQUE(name)", "Name must be unique")


    @api.onchange("construction_date")
    def _onchange_construction_date(self):
        self.age = (self.construction_date and relativedelta(fields.Date.today(), self.construction_date).days) or 0

    #OVERRIDE

    def _compute_display_name(self):
        # res = super()._compute_display_name()
        for rec in self:
            if rec.construction_date:
                rec.display_name = f"{rec.name} + {rec.construction_date}"
            else:
                rec.display_name = rec.name

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if not rec.age:
                rec._onchange_construction_date()
        return records

    #ACTIONS

    def action_create_room(self):
        self.ensure_one()
        action = self.env.ref("eagle_estates.eagle_property_rooms_actions").read()[0]
        action["context"] = {"default_property_id": self.id}
        action["views"] = [(False, "form")]
        return action

    def action_view_rooms(self):
        self.ensure_one()
        return self.room_ids._get_records_action()
