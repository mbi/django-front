(function(jQuery){
    window.front_edit_plugin = {

        target: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            return '<div class="front-edit-container" id="edit-'+ element_id +'"></div>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            this.target = target;
            this.target.find('.front-edit-container').html(html);
            var editor_options = jQuery.extend({
                toolbar: {
                    buttons: ['bold', 'italic', 'underline', 'anchor', 'h1', 'h2', 'h3', 'quote', 'removeFormat'],
                }
            }, front_edit_options.editor_options);
            var editor = new MediumEditor('.front-edit-container', editor_options);
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            return this.target.find('.front-edit-container').html();
        },

        // destroy the editor
        destroy_editor: function() {
            self.target = null;
        }

    };
})(jQuery);
