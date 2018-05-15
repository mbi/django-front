(function(jQuery){
    window.front_edit_plugin = {

        element_id: null,
        editor: null,

        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<div class="front-edit-container" id="edit-'+ this.element_id +'"></div>';
        },

        set_html: function(target, html, front_edit_options) {
            if (this.editor === null) {
                var editor_options = jQuery.extend({
                    height: 300,
                    minHeight: null,
                    maxHeight: null,
                    focus: true
                }, front_edit_options.editor_options);
                this.editor = jQuery('#edit-'+ this.element_id).summernote(editor_options);
            }

            this.editor.summernote('code', html);
        },

        get_html: function(front_edit_options) {
            return this.editor.summernote('code');
        },

        // destroy the editor
        destroy_editor: function() {
            if (this.editor !== null) {
                this.editor.summernote('destroy');
                this.editor = null;
            }
        }
    };
})(jQuery);
