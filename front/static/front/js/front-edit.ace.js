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
            var this_ = this;
            this_.target = target;
            jQuery.getScript('https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.9/ace.js', function(){
                this_.target.addClass('front-edit-ace');
                this_.editor = ace.edit("edit-" + this_.element_id);
                this_.editor.setTheme("ace/theme/monokai");
                this_.editor.$blockScrolling = Infinity;
                this_.editor.setValue(html, -1);
                this_.editor.getSession().setMode("ace/mode/html");
                this_.editor.getSession().setUseWrapMode(true);
            });
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
