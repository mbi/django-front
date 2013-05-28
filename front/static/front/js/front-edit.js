jQuery(document).ready(function($) {
    var editables = $('.editable');

    editables.on('dblclick', function(event) {
        event.preventDefault();

        var el = $(this),
            body = $('body'),
            html = el.html(),
            el_id = el.attr('id'),
            tag = 'textarea',
            plugin = document._front_edit.plugin,
            container,
            editor,
            target;


        if (plugin == 'ace') {
            tag = 'div';
        }

        // this will contain the actual editor block
        container = $('<'+tag+' class="front-edit-container" id="edit-'+el_id+'"></'+tag+'><p class="front-edit-buttons"><button class="cancel">cancel</button><button class="save">save</button></p>');

        if(body.is('.front-editing')) {
            return;
        }
        body.addClass('front-editing');


        switch(document._front_edit.edit_mode) {
            case 'inline':
                el.html(container);
                target = el;
                break;

            case 'lightbox':
                $('<div id="front-edit-lightbox-container" class="active front-edit-dialog_layer front-edit-layer"><div id="front-edit-lightbox" class="front-edit-dialog"></div></div>').appendTo($('body'));
                var lightbox = $('#front-edit-lightbox');
                lightbox.html(container);
                target = lightbox;
                break;
        }


        switch(plugin) {
            case 'ace':
                $.getScript('http://d1n0x3qji82z53.cloudfront.net/src-min-noconflict/ace.js', function(){
                    target.addClass('front-edit-ace');
                    editor = ace.edit("edit-" + el_id);
                    editor.setTheme("ace/theme/monokai");
                    editor.setValue(html);
                    editor.getSession().setMode("ace/mode/html");
                    editor.getSession().setUseWrapMode(true);
                });
                break;
            case 'wymeditor':
                target.find('.front-edit-container').html(html);
                $.getScript(document._front_edit.static_root+'wymeditor/jquery.wymeditor.min.js', function(){
                    target.addClass('front-edit-wym');
                    var base_path = document._front_edit.static_root+'wymeditor/';
                    $('#edit-' + el_id).wymeditor({
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
                        skinPath: document._front_edit.static_root + 'wym/django/'

                    });
                });


                break;
            case 'redactor':
                target.find('.front-edit-container').html(html).redactor();
                break;
            default:
                target.find('.front-edit-container').html(html);
                break;
        }

        target.find('.cancel').on('click', function(event) {
            el.html(html);
            body.removeClass('front-editing');
            $('#front-edit-lightbox-container').remove();
        });

        target.find('.save').on('click', function(event) {
            var new_html, key = el_id;

            switch(plugin) {
                case 'ace':
                    new_html = editor.getValue();
                    break;
                case 'wymeditor':
                    new_html = $.wymeditors(0).xhtml();
                    break;
                case 'redactor':
                    try {
                        // redactor 0.8+
                        new_html = target.find('.front-edit-container').getCode();
                    } catch(err) {
                        // redactor 0.9+
                        new_html = target.find('.front-edit-container').redactor('get');
                    }

                    break;
                default:
                    new_html = target.find('.front-edit-container').val();
                    break;
            }

            $.post(document._front_edit.save_url, {
                key: key,
                val: new_html,
                csrfmiddlewaretoken: document._front_edit.csrf_token
            }, function(data, textStatus, xhr) {
                // todo: return val
            });
            body.removeClass('front-editing');
            el.html(new_html);
            $('#front-edit-lightbox-container').remove();
        });
    });
});
