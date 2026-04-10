from odoo import api, fields, models


class EaglePropertyRoomAreaWizard(models.TransientModel):
    _name = "eagle.property.room.area.wizard"
    _description = "Eagle Property Room Area Wizard"

    length = fields.Float()
    width = fields.Float()
    area = fields.Float(compute="_compute_area")
    room_id = fields.Many2one("eagle.property.room")

    @api.depends("length", "width")
    def _compute_area(self):
        for rec in self:
            rec.area = rec.length * rec.width

    def action_save(self):
        self.room_id.area = self.area
        return {"type": "ir.actions.act_window_close"}
