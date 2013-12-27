var front_edit_plugin = {

    target: null,

    get_container_html: function(element_id, front_edit_options) {
        return '<textarea class="front-edit-container" id="edit-'+ element_id +'"></textarea>';
    },

    set_html: function(target, html, front_edit_options) {
        this.target = target;

        this.target.addClass('front-edit-redactor');
        var editor_options = $.extend({minHeight:400}, front_edit_options.editor_options);
        this.target.find('.front-edit-container').html(html).redactor(editor_options);
    },

    get_html: function(front_edit_options) {
        var new_html = null;
        try {
            // redactor 0.8+
            new_html = this.target.find('.front-edit-container').getCode();
        } catch(err) {
            // redactor 0.9+
            new_html = this.target.find('.front-edit-container').redactor('get');
        }

        return new_html;
    }

};