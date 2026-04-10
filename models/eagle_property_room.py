from odoo import models, fields


class EaglePropertyRoom(models.Model):
    _name = "eagle.property.room"
    _description = "Eagle Property Room"

    room_type = fields.Selection([("living", "Living"), ("bedroom", "Bedroom"), ("bathroom", "Bathroom"), ("garage", "Garage"), ("other", "Other"), ("dining", "Dining"), ("kitchen", "Kitchen")])
    area = fields.Float()
    property_id = fields.Many2one(comodel_name="eagle.property")

    street = fields.Char(related="property_id.street")
    zip = fields.Char(related='property_id.zip')
    city = fields.Char(related="property_id.city")
    state_id = fields.Many2one(comodel_name="res.country.state", related='property_id.state_id')
    country_id = fields.Many2one(related="property_id.country_id")

    construction_date = fields.Date(related="property_id.construction_date")


    def action_open_area_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "eagle.property.room.area.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_room_id": self.id},
        }
