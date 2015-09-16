(function(jQuery){
    window.front_edit_plugin = {

        element_id: null,
        editor: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            this.element_id = "edit-"+ element_id;
            return '<textarea name="'+ this.element_id +'" rows="10" cols="80" class="front-edit-container" id="'+ this.element_id +'"></textarea>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            try {
                this.editor.setData(html);
            } catch(err) {
                jQuery('#'+ this.element_id).html(html);
                this.editor = CKEDITOR.replace(this.element_id, front_edit_options.editor_options);
            }
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            return this.editor.getData();
        },

        // destroy the editor
        destroy_editor: function() {
            this.editor.destroy();
            this.editor = null;
            this.element_id = null;
        }
    };
})(jQuery);
