; (function ($, window, document, undefined) {
    var pluginName = "jkeyboard",
        defaults = {
            layout: "english",
            selectable: ['azeri', 'english'],
            input: $('#input'),
            customLayouts: {
                selectable: []
            },
        };

    var function_keys = {
        backspace: {
            text: 'bksp',
        },
        return: {
            text: 'Enter'
        },
        shift: {
            text: 'shift'
        },
        space: {
            text: '&nbsp;'
        },
        numeric_switch: {
            text: '123',
            command: function () {
                this.createKeyboard('numeric');
                this.events();
            }
        },
        character_switch: {
            text: 'ABC',
            command: function () {
                this.createKeyboard(layout);
                this.events();
            }
        },
        symbol_switch: {
            text: '#+=',
            command: function () {
                this.createKeyboard('symbolic');
                this.events();
            }
        }
    };


    var layouts = {
        azeri: [
            ['q', 'ü', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'ö', 'ğ'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ı', 'ə'],
            ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'ç', 'ş', 'backspace'],
            ['numeric_switch', 'space', 'return']
        ],
        english: [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',],
            ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'backspace'],
            ['numeric_switch', 'space', 'return']
        ],
        numeric: [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['-', '/', ':', ';', '(', ')', '$', '&', '@', '"'],
            ['symbol_switch', '.', ',', '?', '!', "'", 'backspace'],
            ['character_switch', 'space', 'return'],
        ],
        symbolic: [
            ['[', ']', '{', '}', '#', '%', '^', '*', '+', '='],
            ['_', '\\', '|', '~', '<', '>'],
            ['numeric_switch', '.', ',', '?', '!', "'", 'backspace'],
            ['character_switch', 'space', 'return'],

        ]
    }

    var shift = false, capslock = false, layout = 'english', layout_id = 0;

    function Plugin(element, options) {
        this.element = element;
        this.settings = $.extend({}, defaults, options);
        layouts = $.extend(true, {}, this.settings.customLayouts, layouts);
        if (Array.isArray(this.settings.customLayouts.selectable)) {
            $.merge(this.settings.selectable, this.settings.customLayouts.selectable);
        }
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    Plugin.prototype = {
        init: function () {
            layout = this.settings.layout;
            this.createKeyboard(layout);
            this.events();
        },

        setInput: function (newInputField) {
            this.settings.input = newInputField;
        },

        createKeyboard: function (layout) {
            shift = false;
            capslock = false;

            var keyboard_container = $('<ul/>').addClass('jkeyboard'),
                me = this;

            layouts[layout].forEach(function (line, index) {
                var line_container = $('<li/>').addClass('jline');
                line_container.append(me.createLine(line));
                keyboard_container.append(line_container);
            });

            $(this.element).html('').append(keyboard_container);
        },

        createLine: function (line) {
            var line_container = $('<ul/>');

            line.forEach(function (key, index) {
                var key_container = $('<li/>').addClass('jkey').data('command', key);

                if (function_keys[key]) {
                    key_container.addClass(key).html(function_keys[key].text);
                }
                else {
                    key_container.addClass('letter').html(key);
                }

                line_container.append(key_container);
            })

            return line_container;
        },

        events: function () {
            var letters = $(this.element).find('.letter'),
                shift_key = $(this.element).find('.shift'),
                space_key = $(this.element).find('.space'),
                backspace_key = $(this.element).find('.backspace'),
                return_key = $(this.element).find('.return'),

                me = this,
                fkeys = Object.keys(function_keys).map(function (k) {
                    return '.' + k;
                }).join(',');

            letters.on('click', function () {
                me.type((shift || capslock) ? $(this).text().toUpperCase() : $(this).text());
            });

            space_key.on('click', function () {
                me.type(' ');
            });

            return_key.on('click', function () {
                me.type("\n");
                me.settings.input.parents('form').submit();
            });

            backspace_key.on('click', function () {
                me.backspace();
            });

            shift_key.on('click', function () {
                if (shift) {
                    me.toggleShiftOff();
                } else {
                    me.toggleShiftOn();
                }
            }).on('dblclick', function () {
                me.toggleShiftOn(true);
            });


            $(fkeys).on('click', function (e) {
                //prevent bubbling to avoid side effects when used as floating keyboard which closes on click outside of keyboard container
                e.stopPropagation();
                
                var command = function_keys[$(this).data('command')].command;
                if (!command) return;

                command.call(me);
            });
        },

        type: function (key) {
            var input = this.settings.input,
                val = input.val(),
                input_node = input.get(0),
                start = input_node.selectionStart,
                end = input_node.selectionEnd;

            var max_length = $(input).attr("maxlength");
            if (start == end && end == val.length) {
                if (!max_length || val.length < max_length) {
                    input.val(val + key);
                }
            } else {
                var new_string = this.insertToString(start, end, val, key);
                input.val(new_string);
                start++;
                end = start;
                input_node.setSelectionRange(start, end);
            }

            input.trigger('focus');

            if (shift && !capslock) {
                this.toggleShiftOff();
            }
        },

        backspace: function () {
            var input = this.settings.input,
                input_node = input.get(0),
                start = input_node.selectionStart,
                val = input.val();    

            if (start > 0) {
                input.val(val.substring(0, start - 1) + val.substring(start));
                input.trigger('focus');
                input_node.setSelectionRange(start - 1, start - 1);
            }
            else {
                input.trigger('focus');
                input_node.setSelectionRange(0, 0);
            }
	    },

        toggleShiftOn: function (lock) {
            var letters = $(this.element).find('.letter'),
                shift_key = $(this.element).find('.shift');

            letters.addClass('uppercase');
            shift_key.addClass('active');
            if (typeof lock !== 'undefined' && lock) {
                shift_key.addClass('lock');
                capslock = true;
            }
            shift = true;
        },

        toggleShiftOff: function () {
            var letters = $(this.element).find('.letter'),
                shift_key = $(this.element).find('.shift');

            letters.removeClass('uppercase');
            shift_key.removeClass('active lock');
            shift = capslock = false;
        },
        insertToString: function (start, end, string, insert_string) {
            return string.substring(0, start) + insert_string + string.substring(end, string.length);
        }
    };


    var methods = {
        init: function(options) {
            if (!this.data("plugin_" + pluginName)) {
                this.data("plugin_" + pluginName, new Plugin(this, options));
            }
        },
        setInput: function(content) {
            this.data("plugin_" + pluginName).setInput($(content));
        },
    };

    $.fn[pluginName] = function (methodOrOptions) {
        if (methods[methodOrOptions]) {
            return methods[methodOrOptions].apply(this.first(), Array.prototype.slice.call( arguments, 1));
        } else if (typeof methodOrOptions === 'object' || ! methodOrOptions) {
            // Default to "init"
            return methods.init.apply(this.first(), arguments);
        } else {
            $.error('Method ' +  methodOrOptions + ' does not exist on jQuery.jkeyboard');
        }
    };

})(jQuery, window, document);
