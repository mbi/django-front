(function(jQuery){
    window.front_edit_plugin = {

        target: null,
        editor: null,
        element_id: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<div class="front-edit-container" id="edit-'+ this.element_id +'"></div>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            this.target = target;

            this.target.addClass('front-edit-ace');
            this.editor = ace.edit("edit-" + this.element_id);
            this.editor.setTheme("ace/theme/tomorrow_night");
            this.editor.getSession().setValue(html, -1);
            this.editor.getSession().setMode("ace/mode/html");
            this.editor.getSession().setUseWrapMode(true);
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            return this.editor.getValue();
        },

        // destroy the editor
        destroy_editor: function() {
            self.target = null;
            self.editor = null;
            self.element_id = null;
        }

    };
})(jQuery);
