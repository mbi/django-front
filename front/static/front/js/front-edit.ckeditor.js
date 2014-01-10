var front_edit_plugin = {

    target: null,
    target_id: null,

    // Returns the html that will contain the editor
    get_container_html: function(element_id, front_edit_options) {
        this.element_id = element_id;
        return '<textarea name="edit-'+ element_id +'" rows="10" cols="80" class="front-edit-container" id="edit-'+ element_id +'"></textarea>';
    },

    // initializes the editor on the target element, with the given html code
    set_html: function(target, html, front_edit_options) {
        this.target = target;
        $('#edit-'+ this.element_id).html(html);
        CKEDITOR.replace('edit-'+ this.element_id);
    },

    // returns the edited html code
    get_html: function(front_edit_options) {
        return this.target.find('.front-edit-container').val();
    },

    // destroy the editor
    destroy_editor: function() {
        self.target = null;
    }

};