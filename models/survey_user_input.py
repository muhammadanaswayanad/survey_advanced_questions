from odoo import api, fields, models, _
import json

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'
    
    # No specific field additions needed here, we'll use existing mechanisms


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'
    
    # Fields for advanced answer types
    fill_blank_answers = fields.Text('Fill Blank Answers')
    match_answers = fields.Text('Match Answers')
    drag_drop_answers = fields.Text('Drag and Drop Answers')
    
    @api.depends('question_id.question_type', 'fill_blank_answers', 'match_answers', 
                 'drag_drop_answers', 'answer_type')
    def _compute_value_count(self):
        super(SurveyUserInputLine, self)._compute_value_count()
        for line in self:
            if line.question_id.question_type == 'fill_blank' and line.fill_blank_answers:
                # Each blank counts as one answer
                try:
                    line.value_count = len(json.loads(line.fill_blank_answers))
                except:
                    line.value_count = 0
            elif line.question_id.question_type == 'matching' and line.match_answers:
                try:
                    line.value_count = len(json.loads(line.match_answers))
                except:
                    line.value_count = 0
            elif line.question_id.question_type == 'drag_drop' and line.drag_drop_answers:
                try:
                    line.value_count = len(json.loads(line.drag_drop_answers))
                except:
                    line.value_count = 0

    @api.depends('question_id.question_type', 'value_numerical_box', 'value_date',
                 'value_text_box', 'value_char_box', 'suggested_answer_id', 'value_datetime',
                 'fill_blank_answers', 'match_answers', 'drag_drop_answers')
    def _compute_answer_score(self):
        super(SurveyUserInputLine, self)._compute_answer_score()
        for line in self:
            score = 0.0
            
            # Handle advanced types scoring
            if line.question_id.question_type == 'fill_blank' and line.fill_blank_answers:
                try:
                    user_answers = json.loads(line.fill_blank_answers)
                    correct_answers = line.question_id.fill_blank_answer_ids
                    
                    if len(user_answers) == len(correct_answers):
                        for i, answer in enumerate(user_answers):
                            if i >= len(correct_answers):
                                continue
                                
                            correct = correct_answers[i]
                            if correct.is_case_sensitive:
                                is_correct = (answer == correct.correct_answer)
                            else:
                                is_correct = (answer.lower() == correct.correct_answer.lower())
                                
                                # Check allowed variations
                                if not is_correct and correct.allowed_variations:
                                    variations = [v.strip().lower() for v in correct.allowed_variations.split(',')]
                                    is_correct = answer.lower() in variations
                                    
                            if is_correct:
                                score += 1.0
                                
                        # Calculate percentage score
                        score = (score / len(correct_answers)) * line.question_id.answer_score
                except:
                    score = 0.0
                    
            elif line.question_id.question_type == 'matching' and line.match_answers:
                try:
                    user_matches = json.loads(line.match_answers)
                    correct_items = line.question_id.match_item_ids
                    
                    correct_matches = 0
                    correct_dict = {item.left_text: item.right_text for item in correct_items}
                    
                    for left, right in user_matches.items():
                        if left in correct_dict and correct_dict[left] == right:
                            correct_matches += 1
                    
                    if correct_items:
                        score = (correct_matches / len(correct_items)) * line.question_id.answer_score
                except:
                    score = 0.0
                    
            elif line.question_id.question_type == 'drag_drop' and line.drag_drop_answers:
                try:
                    user_placements = json.loads(line.drag_drop_answers)
                    drag_items = {str(item.id): item for item in line.question_id.drag_item_ids}
                    
                    correct_placements = 0
                    total_items = len(drag_items)
                    
                    for item_id, zone_id in user_placements.items():
                        if (item_id in drag_items and 
                            drag_items[item_id].correct_drop_zone_id and 
                            str(drag_items[item_id].correct_drop_zone_id.id) == zone_id):
                            correct_placements += 1
                    
                    if total_items > 0:
                        score = (correct_placements / total_items) * line.question_id.answer_score
                except:
                    score = 0.0
            
            if line.question_id.question_type in ['fill_blank', 'matching', 'drag_drop']:
                line.answer_score = score
