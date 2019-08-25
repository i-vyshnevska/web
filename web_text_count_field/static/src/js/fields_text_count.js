odoo.define('text_count', function(require) {
    "use strict";

    require('web.dom_ready');
    var registry = require('web.field_registry');
    var basicFields = require('web.basic_fields');
    var FieldText = basicFields.FieldText;

    var FieldTextCount = FieldText.extend({
        events: _.extend({}, FieldText.prototype.events, {
            'input': 'count_char',
        }),
        supportedFieldTypes: ['text'],

        start: function () {
            
            var self = this;
            return this._super().then(function(){
                if (self.mode === 'edit') {
                    if (self.attrs.size) {
                        // this place can be improved should relay on self.field.size
                        self.$el.attr('maxlength', parseInt(self.attrs.size));
                    }
                    self.$el = self.$el.add($('<input class="text-counter" readonly="readonly"/>'));
                }
            });
        },

        count_char: function (e) {
            var $textarea = this.$el,
                maxlength = parseInt($textarea.attr('maxlength'), 10),
                $counter = $textarea.siblings('.text-counter');
            var left = maxlength - $textarea.val().length;
            if (left < 0) {
                left = 0;
            }
            $counter.val(left);
        },

    });

    registry.add('text_count', FieldTextCount);
});
