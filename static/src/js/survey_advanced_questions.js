odoo.define('survey_advanced_questions.frontend', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var surveyForm = require('survey.form');

    // Extend survey form widget
    surveyForm.include({
        events: _.extend({}, surveyForm.prototype.events, {
            'change .fill-blank-input': '_onFillBlankChange',
            'click .matching-right-option': '_onMatchOptionClick',
            'dragstart .drag-item': '_onDragStart',
            'dragover .drop-zone': '_onDragOver',
            'drop .drop-zone': '_onDrop',
            'dragleave .drop-zone': '_onDragLeave',
        }),
        
        /**
         * Initialize advanced question features after DOM ready
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._initMatchingQuestions();
                self._initDragAndDropQuestions();
            });
        },

        /**
         * Initialize matching questions
         */
        _initMatchingQuestions: function () {
            var self = this;
            $('.matching-container').each(function () {
                var $container = $(this);
                var questionId = $container.data('question-id');
                
                // Make right items clickable and droppable
                $container.find('.matching-right-option').attr('draggable', true);
                
                // Initialize the hidden input
                self._updateMatchingAnswer($container);
            });
        },
        
        /**
         * Initialize drag and drop questions
         */
        _initDragAndDropQuestions: function () {
            var self = this;
            $('.drag-drop-container').each(function () {
                var $container = $(this);
                var questionId = $container.data('question-id');
                
                // Make items draggable
                $container.find('.drag-item').attr('draggable', true);
                
                // Initialize the hidden input
                self._updateDragDropAnswer($container);
            });
        },

        /**
         * Handle fill in the blank changes
         */
        _onFillBlankChange: function (event) {
            var $input = $(event.currentTarget);
            var $container = $input.closest('.fill-blank-container');
            var questionId = $container.data('question-id');
            
            this._updateFillBlankAnswer($container);
        },
        
        /**
         * Handle matching option click
         */
        _onMatchOptionClick: function (event) {
            var $option = $(event.currentTarget);
            var $container = $option.closest('.matching-container');
            var selectedLeftItem = $container.find('.matching-left-item.selected');
            
            if (selectedLeftItem.length) {
                var leftText = selectedLeftItem.data('left-text');
                var rightText = $option.data('right-text');
                
                // Mark this pair as matched
                selectedLeftItem.attr('data-matched-to', rightText);
                selectedLeftItem.removeClass('selected').addClass('matched');
                
                this._updateMatchingAnswer($container);
            }
        },
        
        /**
         * Handle drag start
         */
        _onDragStart: function (event) {
            var $item = $(event.currentTarget);
            event.originalEvent.dataTransfer.setData('text/plain', $item.data('item-id'));
            event.originalEvent.dataTransfer.effectAllowed = 'move';
        },
        
        /**
         * Handle drag over
         */
        _onDragOver: function (event) {
            event.preventDefault();
            $(event.currentTarget).addClass('drag-over');
            event.originalEvent.dataTransfer.dropEffect = 'move';
        },
        
        /**
         * Handle drop
         */
        _onDrop: function (event) {
            event.preventDefault();
            var $zone = $(event.currentTarget);
            var $container = $zone.closest('.drag-drop-container');
            var itemId = event.originalEvent.dataTransfer.getData('text/plain');
            var zoneId = $zone.data('zone-id');
            
            // Move the item visually
            var $item = $container.find(`.drag-item[data-item-id="${itemId}"]`);
            $item.detach();
            $zone.find('.zone-items').append($item);
            $item.attr('data-placed-in', zoneId);
            
            $zone.removeClass('drag-over');
            
            this._updateDragDropAnswer($container);
        },
        
        /**
         * Handle drag leave
         */
        _onDragLeave: function (event) {
            $(event.currentTarget).removeClass('drag-over');
        },

        /**
         * Update the hidden input with fill in the blank answers
         */
        _updateFillBlankAnswer: function ($container) {
            var questionId = $container.data('question-id');
            var answers = [];
            
            $container.find('.fill-blank-input').each(function () {
                answers.push($(this).val());
            });
            
            var inputName = `fill_blank_answers_${questionId}`;
            var $hiddenInput = $(`#${inputName}`);
            
            // Create hidden input if it doesn't exist
            if (!$hiddenInput.length) {
                $container.append($('<input>', {
                    type: 'hidden',
                    name: inputName,
                    id: inputName
                }));
                $hiddenInput = $(`#${inputName}`);
            }
            
            $hiddenInput.val(JSON.stringify(answers));
        },
        
        /**
         * Update the hidden input with matching answers
         */
        _updateMatchingAnswer: function ($container) {
            var questionId = $container.data('question-id');
            var matches = {};
            
            $container.find('.matching-item[data-matched-to]').each(function () {
                var leftText = $(this).data('left-text');
                var rightText = $(this).data('matched-to');
                matches[leftText] = rightText;
            });
            
            var inputId = `match_answers_${questionId}`;
            $(`#${inputId}`).val(JSON.stringify(matches));
        },
        
        /**
         * Update the hidden input with drag and drop answers
         */
        _updateDragDropAnswer: function ($container) {
            var questionId = $container.data('question-id');
            var placements = {};
            
            $container.find('.drag-item[data-placed-in]').each(function () {
                var itemId = $(this).data('item-id');
                var zoneId = $(this).data('placed-in');
                placements[itemId] = zoneId;
            });
            
            var inputId = `drag_drop_answers_${questionId}`;
            $(`#${inputId}`).val(JSON.stringify(placements));
        },

        /**
         * Extend prepare form data submission to include our custom question types
         */
        _prepareSubmitValues: function () {
            var self = this;
            var result = this._super.apply(this, arguments);
            
            // Process fill in the blanks
            $('.fill-blank-container').each(function () {
                var $container = $(this);
                var questionId = $container.data('question-id');
                var inputId = `fill_blank_answers_${questionId}`;
                var answers = $(`#${inputId}`).val();
                
                if (answers) {
                    result[`question_${questionId}`] = {
                        'fill_blank_answers': answers
                    };
                }
            });
            
            // Process matching questions
            $('.matching-container').each(function () {
                var $container = $(this);
                var questionId = $container.data('question-id');
                var inputId = `match_answers_${questionId}`;
                var answers = $(`#${inputId}`).val();
                
                if (answers) {
                    result[`question_${questionId}`] = {
                        'match_answers': answers
                    };
                }
            });
            
            // Process drag and drop questions
            $('.drag-drop-container').each(function () {
                var $container = $(this);
                var questionId = $container.data('question-id');
                var inputId = `drag_drop_answers_${questionId}`;
                var answers = $(`#${inputId}`).val();
                
                if (answers) {
                    result[`question_${questionId}`] = {
                        'drag_drop_answers': answers
                    };
                }
            });
            
            return result;
        }
    });

    return {
        // Export functionality if needed
    };
});
