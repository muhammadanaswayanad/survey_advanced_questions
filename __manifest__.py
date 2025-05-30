{
    'name': 'Survey Advanced Questions',
    'version': '17.0.1.0.0',
    'summary': 'Extended question types for Odoo Survey',
    'description': """
        Advanced question types for Odoo surveys:
        - Fill in the Blanks
        - Match the Following
        - Drag and Drop
    """,
    'category': 'Marketing/Surveys',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_question_views.xml',
        'views/survey_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/survey_advanced_questions/static/src/js/survey_advanced_questions.js',
            '/survey_advanced_questions/static/src/scss/survey_advanced_questions.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
