(function(jQuery){
    window.front_edit_plugin = {

        target: null,
        editor: null,
        element_id: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<textarea class="front-edit-container" id="edit-'+ this.element_id +'"></textarea>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            this.target = target;
            var this_ = this;

            try {
                jQuery.wymeditors(0).html(html);
            } catch(err) {
                this_.target.find('.front-edit-container').html(html);
                jQuery.getScript(front_edit_options.static_root + 'wymeditor/jquery.wymeditor.min.js', function(){
                    this_.target.addClass('front-edit-wym');
                    var base_path = front_edit_options.static_root+'wymeditor/';
                    var editor_options = jQuery.extend({
                        updateSelector: "input:submit",
                        updateEvent: "click",
                        logoHtml: '',
                        skin: 'django',
                        classesItems: [
                            {'name': 'image', 'title': 'DIV: Image w/ Caption', 'expr': 'div'},
                            {'name': 'caption', 'title': 'P: Caption', 'expr': 'p'},
                            {'name': 'align-left', 'title': 'Float: Left', 'expr': 'p, div, img'},
                            {'name': 'align-right', 'title': 'Float: Right', 'expr': 'p, div, img'}
                        ],
                        basePath: base_path,
                        wymPath: base_path + 'jquery.wymeditor.min.js',
                        skinPath: front_edit_options.static_root + 'wym/django/'

                    }, front_edit_options.editor_options);
                    jQuery('#edit-' + this_.element_id).wymeditor(editor_options);
                });
            }
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            return jQuery.wymeditors(0).xhtml();
        },

        // destroy the editor
        destroy_editor: function() {
            self.target = null;
            self.editor = null;
            self.element_id = null;
            jQuery.wymeditors = null;
        }
    };
})(jQuery);
