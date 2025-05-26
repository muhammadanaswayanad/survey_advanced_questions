odoo.define('survey_advanced_questions.frontend', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;

publicWidget.registry.SurveyAdvancedQuestions = publicWidget.Widget.extend({
    selector: '.o_survey_form',
    events: {
        'dragstart .drag_item': '_onDragStart',
        'dragover .drop_zone': '_onDragOver',
        'drop .drop_zone': '_onDrop',
        'click .match_right_item': '_onMatchItemClick',
    },
    
    /**
     * @override
     */
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            self._initializeFillBlanks();
            self._initializeMatchFollowing();
            self._initializeDragDrop();
        });
    },
    
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    
    /**
     * Initialize fill in the blanks questions
     * 
     * @private
     */
    _initializeFillBlanks: function () {
        var self = this;
        // Find all fill in the blank questions
        this.$el.find('.fill_blank_container').each(function () {
            var $container = $(this);
            var text = $container.text().trim();
            
            // Replace [___] with input fields
            var html = text.replace(/\[___\]/g, '<input type="text" class="fill_blank_input" />');
            $container.html(html);
        });
    },
    
    /**
     * Initialize match the following questions
     * 
     * @private
     */
    _initializeMatchFollowing: function () {
        var self = this;
        // Find all match the following questions
        this.$el.find('.match_following_container').each(function () {
            var $container = $(this);
            
            // Randomize right items
            var $rightItems = $container.find('.match_right_items').children().toArray();
            $rightItems.sort(function() { return 0.5 - Math.random(); });
            $container.find('.match_right_items').empty().append($rightItems);
            
            // Initialize matching state
            $container.data('matches', {});
        });
    },
    
    /**
     * Initialize drag and drop questions
     * 
     * @private
     */
    _initializeDragDrop: function () {
        var self = this;
        // Find all drag and drop questions
        this.$el.find('.drag_drop_container').each(function () {
            var $container = $(this);
            
            // Initialize placement state
            $container.data('placements', {});
        });
    },
    
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    
    /**
     * Handle drag start event
     * 
     * @private
     * @param {Event} ev
     */
    _onDragStart: function (ev) {
        ev.originalEvent.dataTransfer.setData('text/plain', $(ev.currentTarget).data('item-id'));
        ev.originalEvent.dataTransfer.effectAllowed = 'move';
    },
    
    /**
     * Handle drag over event
     * 
     * @private
     * @param {Event} ev
     */
    _onDragOver: function (ev) {
        ev.preventDefault();
        ev.originalEvent.dataTransfer.dropEffect = 'move';
        $(ev.currentTarget).addClass('drag-over');
    },
    
    /**
     * Handle drop event
     * 
     * @private
     * @param {Event} ev
     */
    _onDrop: function (ev) {
        ev.preventDefault();
        var $dropZone = $(ev.currentTarget);
        $dropZone.removeClass('drag-over');
        
        var itemId = ev.originalEvent.dataTransfer.getData('text/plain');
        var zoneId = $dropZone.data('zone-id');
        
        // Update placements
        var $container = $dropZone.closest('.drag_drop_container');
        var placements = $container.data('placements') || {};
        placements[itemId] = zoneId;
        $container.data('placements', placements);
        
        // Update UI
        var $item = this.$el.find('.drag_item[data-item-id="' + itemId + '"]');
        $dropZone.append($item);
        
        // Store the answer in a hidden input for form submission
        var $question = $container.closest('.o_survey_question');
        var questionId = $question.data('question-id');
        var $input = $question.find('input.drag_drop_answers');
        if (!$input.length) {
            $input = $('<input type="hidden" class="drag_drop_answers" />').appendTo($question);
        }
        $input.val(JSON.stringify(placements));
    },
    
    /**
     * Handle clicking on a match item
     * 
     * @private
     * @param {Event} ev
     */
    _onMatchItemClick: function (ev) {
        var $rightItem = $(ev.currentTarget);
        var $container = $rightItem.closest('.match_following_container');
        var $leftItem = $container.find('.match_left_item.selected');
        
        if ($leftItem.length) {
            // Make the match
            var leftId = $leftItem.data('item-id');
            var rightId = $rightItem.data('item-id');
            
            // Update matches
            var matches = $container.data('matches') || {};
            matches[leftId] = rightId;
            $container.data('matches', matches);
            
            // Update UI
            $leftItem.removeClass('selected').addClass('matched');
            $rightItem.addClass('matched');
            
            // Store the answer in a hidden input for form submission
            var $question = $container.closest('.o_survey_question');
            var questionId = $question.data('question-id');
            var $input = $question.find('input.match_answers');
            if (!$input.length) {
                $input = $('<input type="hidden" class="match_answers" />').appendTo($question);
            }
            $input.val(JSON.stringify(matches));
        }
    }
});

return publicWidget.registry.SurveyAdvancedQuestions;

});
