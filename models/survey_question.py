from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection(
        selection_add=[
            ('fill_blank', 'Fill in the Blanks'),
            ('match_following', 'Match the Following'),
            ('drag_drop', 'Drag and Drop')
        ],
        ondelete={
            'fill_blank': 'cascade',  # Changed from 'set default' to 'cascade'
            'match_following': 'cascade',  # Changed from 'set default' to 'cascade'
            'drag_drop': 'cascade'  # Changed from 'set default' to 'cascade'
        }
    )
    
    # Fill in the blank fields
    is_fill_in_blank = fields.Boolean(compute='_compute_question_type_fields')
    fill_blank_text = fields.Text(string="Question Text with Blanks", help="Use [___] to indicate blank spaces")
    
    # Match the following fields
    is_match_following = fields.Boolean(compute='_compute_question_type_fields')
    match_item_ids = fields.One2many('survey.question.match.item', 'question_id', string="Match Items")
    
    # Drag and drop fields
    is_drag_drop = fields.Boolean(compute='_compute_question_type_fields')
    drag_item_ids = fields.One2many('survey.question.drag.item', 'question_id', string="Drag Items")
    drop_zone_ids = fields.One2many('survey.question.drop.zone', 'question_id', string="Drop Zones")
    
    @api.depends('question_type')
    def _compute_question_type_fields(self):
        for question in self:
            question.is_fill_in_blank = question.question_type == 'fill_blank'
            question.is_match_following = question.question_type == 'match_following'
            question.is_drag_drop = question.question_type == 'drag_drop'

    @api.constrains('question_type', 'fill_blank_text', 'fill_blank_answer_ids')
    def _check_fill_blank_answers(self):
        for question in self:
            if question.question_type == 'fill_blank':
                # Count blanks in text
                blanks_count = question.fill_blank_text.count('[___]') if question.fill_blank_text else 0
                answers_count = len(question.fill_blank_answer_ids)
                
                if blanks_count != answers_count:
                    raise ValidationError(_("The number of blanks [___] must match the number of answers provided."))

    @api.constrains('question_type', 'match_item_ids')
    def _check_matching_items(self):
        for question in self:
            if question.question_type == 'matching' and len(question.match_item_ids) < 2:
                raise ValidationError(_("A matching question must have at least 2 pairs."))

    @api.constrains('question_type', 'drag_item_ids', 'drop_zone_ids')
    def _check_drag_drop_items(self):
        for question in self:
            if question.question_type == 'drag_drop':
                if not question.drag_item_ids:
                    raise ValidationError(_("You must define at least one drag item."))
                if not question.drop_zone_ids:
                    raise ValidationError(_("You must define at least one drop zone."))


class SurveyQuestionMatchItem(models.Model):
    _name = 'survey.question.match.item'
    _description = 'Survey Question Match Item'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete="cascade")
    left_text = fields.Char(string="Left Item", required=True)
    right_text = fields.Char(string="Matching Option", required=True)


class SurveyQuestionDragItem(models.Model):
    _name = 'survey.question.drag.item'
    _description = 'Survey Question Drag Item'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete="cascade")
    item_text = fields.Char(string="Draggable Item", required=True)
    correct_zone_id = fields.Many2one('survey.question.drop.zone', string="Correct Drop Zone")


class SurveyQuestionDropZone(models.Model):
    _name = 'survey.question.drop.zone'
    _description = 'Survey Question Drop Zone'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete="cascade")
    zone_text = fields.Char(string="Drop Zone Text", required=True)
