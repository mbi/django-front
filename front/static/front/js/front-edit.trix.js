(function(jQuery){
    window.front_edit_plugin = {

        element_id: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<div id="trix-container-'+ element_id +'"><input type="hidden" id="trix-hidden-' + element_id +'"><trix-editor input="trix-hidden-' + element_id +'" class="front-edit-container"></trix-editor></div>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            var editor = document.querySelector("#trix-container-" + this.element_id + " .front-edit-container");
            if (editor && editor.editor) {
                editor.editor.loadHTML(html);
            } else {
                jQuery('#trix-hidden-' + this.element_id).val(html);
            }
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            return jQuery('#trix-hidden-' + this.element_id).val();
        },

        // destroy the editor
        destroy_editor: function() {
            jQuery('#trix-container-'+ this.element_id).remove();
            this.element_id = null;
        }

    };
})(jQuery);
