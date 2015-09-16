(function(jQuery){
    window.front_edit_plugin = {

        target: null,
        editor: null,
        element_id: null,

        // Returns the html that will contain the editor
        get_container_html: function(element_id, front_edit_options) {
            this.element_id = element_id;
            return '<div id="epiceditor"></div>';
        },

        // initializes the editor on the target element, with the given html code
        set_html: function(target, html, front_edit_options) {
            var this_ = this;
            jQuery.when(
                jQuery.getScript(front_edit_options.static_root+'epiceditor/js/epiceditor.min.js'),
                jQuery.getScript(front_edit_options.static_root+'to-markdown/to-markdown.js'),
                jQuery.Deferred(function(deferred) {
                    jQuery(deferred.resolve);
                })
            ).done(function(){
                var opts = jQuery.extend({
                    container: 'epiceditor',
                    textarea: null,
                    basePath: front_edit_options.static_root+'epiceditor',
                    clientSideStorage: false,
                    localStorageName: 'epiceditor',
                    useNativeFullscreen: true,
                    parser: marked,
                    file: {
                        name: 'epiceditor',
                        defaultContent: toMarkdown(html),
                        autoSave: 100
                    },
                    button: {
                        preview: true,
                        fullscreen: true
                    },
                    focusOnLoad: false,
                    shortcut: {
                        modifier: 18,
                        fullscreen: 70,
                        preview: 80
                    },
                    string: {
                        togglePreview: 'Toggle Preview Mode',
                        toggleEdit: 'Toggle Edit Mode',
                        toggleFullscreen: 'Enter Fullscreen'
                    }
                }, front_edit_options.editor_options);
                this_.editor = new EpicEditor(opts).load();
            });
        },

        // returns the edited html code
        get_html: function(front_edit_options) {
            isMarkdown = true;
            return this.editor.exportFile('', 'html');
        },

        // destroy the editor
        destroy_editor: function() {
            self.target = null;
            self.editor = null;
            self.element_id = null;
        }
    };
})(jQuery);
