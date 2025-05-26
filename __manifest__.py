{
    'name': 'Survey Advanced Questions',
    'version': '1.0',
    'category': 'Marketing/Surveys',
    'summary': 'Advanced question types for Odoo Surveys',
    'description': """
        Extends the Odoo Survey module with advanced question types:
        - Fill in the blanks
        - Match the following
        - Drag and drop answers
        
        Enhances user experience and assessment capabilities.
    """,
    'author': 'Odoo Developer',
    'website': 'https://www.example.com',
    'depends': ['survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/survey_question_views.xml',
        'views/survey_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'survey_advanced_questions/static/src/js/survey_advanced_questions.js',
            'survey_advanced_questions/static/src/scss/survey_advanced_questions.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
