from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SurveyQuestion(models.Model):
    _inherit = 'survey.question'

    question_type = fields.Selection(selection_add=[
        ('fill_blank', 'Fill in the Blanks'),
        ('matching', 'Match the Following'),
        ('drag_drop', 'Drag and Drop Answer')
    ], ondelete={'fill_blank': 'cascade', 'matching': 'cascade', 'drag_drop': 'cascade'})
    
    # For fill in the blanks
    fill_blank_text = fields.Text("Text with Blanks", help="Use [___] to denote a blank space")
    fill_blank_answer_ids = fields.One2many('survey.question.fill.blank', 'question_id', string="Fill Blank Answers")
    
    # For matching questions
    match_item_ids = fields.One2many('survey.question.match.item', 'question_id', string="Match Items")
    
    # For drag and drop questions
    drag_item_ids = fields.One2many('survey.question.drag.item', 'question_id', string="Drag Items")
    drop_zone_ids = fields.One2many('survey.question.drop.zone', 'question_id', string="Drop Zones")

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


class SurveyQuestionFillBlank(models.Model):
    _name = 'survey.question.fill.blank'
    _description = 'Survey Question Fill Blank Answer'
    _order = 'sequence, id'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete='cascade', required=True)
    sequence = fields.Integer(default=10)
    correct_answer = fields.Char('Correct Answer', required=True)
    is_case_sensitive = fields.Boolean('Case Sensitive', default=False)
    allowed_variations = fields.Char('Allowed Variations', help="Comma-separated alternative correct answers")


class SurveyQuestionMatchItem(models.Model):
    _name = 'survey.question.match.item'
    _description = 'Survey Question Match Item'
    _order = 'sequence, id'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete='cascade', required=True)
    sequence = fields.Integer(default=10)
    left_text = fields.Char('Left Item', required=True)
    right_text = fields.Char('Right Item', required=True)
    

class SurveyQuestionDragItem(models.Model):
    _name = 'survey.question.drag.item'
    _description = 'Survey Question Drag Item'
    _order = 'sequence, id'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete='cascade', required=True)
    sequence = fields.Integer(default=10)
    name = fields.Char('Item Text', required=True)
    correct_drop_zone_id = fields.Many2one('survey.question.drop.zone', string="Correct Drop Zone")


class SurveyQuestionDropZone(models.Model):
    _name = 'survey.question.drop.zone'
    _description = 'Survey Question Drop Zone'
    _order = 'sequence, id'
    
    question_id = fields.Many2one('survey.question', string="Question", ondelete='cascade', required=True)
    sequence = fields.Integer(default=10)
    name = fields.Char('Zone Label', required=True)
