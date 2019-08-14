odoo.define('text_count', function(require) {
    "use strict";

    require('web.dom_ready');
    var registry = require('web.field_registry');
    var basicFields = require('web.basic_fields');
    var InputField = basicFields.InputField;

    var FieldTextCount = InputField.extend({
        events: _.extend({}, InputField.prototype.events, {
            'input': 'count_char',
        }),
        supportedFieldTypes: ['char'],

        count_char: function (e) {
            $(document).ready(function () {
                    var $self = $(this),
                    maxlength = parseInt($self.attr('maxlength'), 10),
                    length = $self.length,
                    left = maxlength - length,
                    $counter = $self.siblings('.text-counter');

                    if ($self.data('counter')) {
                        $counter = $($self.data('counter'));
                    }
                    if (left < 0) {
                        left = 0;
                    }
                    $counter.val(left);
            });
        },

    });

    registry.add('text_count', FieldTextCount);

});
