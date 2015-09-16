(function(jQuery){
    window.front_edit_plugin = {

        element_id: null,
        editor: null,

        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<textarea class="front-edit-container" id="edit-'+ this.element_id +'"></textarea>';
        },

        set_html: function(target, html, front_edit_options) {
            if (this.editor === null) {
                var editor_options = jQuery.extend({inlineMode: false}, front_edit_options.editor_options);
                this.editor = jQuery('#edit-'+ this.element_id).editable(editor_options);
            }

            this.editor.editable('setHTML', html);
        },

        get_html: function(front_edit_options) {
            return this.editor.editable('getHTML');
        },

        // destroy the editor
        destroy_editor: function() {
            this.editor.editable('destroy');
            this.editor = null;
        }
    };
})(jQuery);
