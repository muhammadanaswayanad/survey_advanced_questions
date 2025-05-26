from odoo import http
from odoo.addons.survey.controllers.main import Survey
import json

class AdvancedSurvey(Survey):
    
    @http.route()
    def submit(self, survey_token, answer_token, **post):
        # Extract advanced question answers from post data
        for key, value in post.items():
            if key.startswith('question_') and isinstance(value, dict):
                # Handle fill in the blanks
                if 'fill_blank_answers' in value:
                    post[key] = {'fill_blank_answers': value['fill_blank_answers']}
                # Handle matching
                elif 'match_answers' in value:
                    post[key] = {'match_answers': value['match_answers']}
                # Handle drag and drop
                elif 'drag_drop_answers' in value:
                    post[key] = {'drag_drop_answers': value['drag_drop_answers']}
                
        return super(AdvancedSurvey, self).submit(survey_token, answer_token, **post)
    
    @http.route()
    def save_line(self, survey_id, answer_token, question_id, **post):
        # Similar handling for partial saves
        for key, value in post.items():
            if key.startswith('question_') and isinstance(value, dict):
                if 'fill_blank_answers' in value:
                    post[key] = {'fill_blank_answers': value['fill_blank_answers']}
                elif 'match_answers' in value:
                    post[key] = {'match_answers': value['match_answers']}
                elif 'drag_drop_answers' in value:
                    post[key] = {'drag_drop_answers': value['drag_drop_answers']}
                
        return super(AdvancedSurvey, self).save_line(survey_id, answer_token, question_id, **post)
