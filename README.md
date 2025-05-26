# Survey Advanced Questions Module for Odoo 17

This module extends Odoo's Survey functionality with advanced question types for more interactive and varied assessments.

## Features

### New Question Types

1. **Fill in the Blanks**
   - Dynamic text with typable blanks
   - Multiple blank spaces in a single question
   - Support for alternative answers and case sensitivity

2. **Match the Following**
   - Two-column interface with items and matching options
   - Drag or click to match left items with right options
   - Visual feedback for matched pairs

3. **Drag and Drop Answers**
   - Draggable elements with drop zones
   - Visual feedback during drag operations
   - Flexible scoring based on correct placements

4. **Standard Multiple Choice** (using existing Odoo functionality)

### Technical Implementation

- Extends `survey.question` model with new question types
- Creates supporting models for advanced question data
- Custom front-end rendering and interaction via JavaScript
- Scoring and validation for all question types

## Module Structure

```
survey_advanced_questions/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── survey_question.py
│   └── survey_user_input.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── views/
│   ├── survey_question_views.xml
│   └── survey_templates.xml
├── static/
│   └── src/
│       ├── js/
│       │   └── survey_advanced_questions.js
│       └── scss/
│           └── survey_advanced_questions.scss
└── security/
    └── ir.model.access.csv
```

## Models

### Extended Models

- `survey.question`: Added new question types and related fields
- `survey.user_input.line`: Extended to handle storage and scoring of advanced answers

### New Models

- `survey.question.fill.blank`: Stores correct answers for fill-in-the-blank questions
- `survey.question.match.item`: Stores matching pairs for matching questions
- `survey.question.drag.item`: Stores draggable items
- `survey.question.drop.zone`: Stores drop zones for drag-and-drop questions

## Frontend Implementation

- JavaScript enhancements for drag-and-drop functionality
- SCSS styling for all question types
- Form submission handling for new answer types
- Mobile-responsive design considerations

## Installation

1. Copy the module to your Odoo addons directory
2. Update the apps list in Odoo
3. Install the module from the Apps menu

## Usage

### Creating Advanced Questions

1. Create a new survey or edit an existing one
2. Add a new question and select the desired question type:
   - Fill in the Blanks
   - Match the Following
   - Drag and Drop Answer
3. Configure the question according to its type

### Fill in the Blanks

1. Enter text with `[___]` to represent blanks
2. Add correct answers for each blank
3. Optionally set case sensitivity and alternative answers

### Match the Following

1. Add item pairs with left and right text
2. The module will automatically randomize the right options when displayed

### Drag and Drop

1. Add drag items and drop zones
2. Specify the correct drop zone for each item

## Technical Notes

### Answer Storage

- Fill in the Blanks: JSON array of answers in `fill_blank_answers` field
- Match the Following: JSON object mapping left to right items in `match_answers` field
- Drag and Drop: JSON object mapping item IDs to zone IDs in `drag_drop_answers` field

### Scoring

Scoring is proportional to the number of correct answers:

- Fill in the Blanks: Score per correct blank
- Match the Following: Score per correct match
- Drag and Drop: Score per correct placement

### Database Tables

The module creates the following tables:
- `survey_question_fill_blank`
- `survey_question_match_item`
- `survey_question_drag_item`
- `survey_question_drop_zone`

## Customization

### Extending the Module

To add more question types:
1. Extend the `question_type` field in `survey_question.py`
2. Create necessary supporting models
3. Add form fields in `survey_question_views.xml`
4. Create frontend templates in `survey_templates.xml`
5. Implement JS handlers in `survey_advanced_questions.js`

### Styling

Customize the appearance by modifying:
- `survey_advanced_questions.scss` for question-specific styles
- `survey_templates.xml` for HTML structure

## Compatibility

- Designed for Odoo 17 Community Edition
- Extends but does not modify core survey functionality
- Works alongside standard survey questions

## Future Development Ideas

- AI-based answer evaluation for fill-in-the-blank questions
- Image-based drag and drop questions
- Timed questions with countdown
- Multi-part questions with dependencies
- Export of detailed question and answer analytics
- PDF export with visual representation of answers

## Troubleshooting

Common issues:
- JavaScript errors: Check browser console and ensure assets are properly loaded
- Drag and drop not working: Verify browser compatibility with HTML5 drag and drop
- Scoring issues: Check the answer validation logic in `survey_user_input.py`

## License

LGPL-3, in line with Odoo Community standards
