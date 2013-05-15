jQuery(document).ready(function($) {
    var editables = $('.editable');

    editables.on('dblclick', function(event) {
        event.preventDefault();

        var el = $(this),
            html = el.html(),
            el_id = el.attr('id'),
            tag = 'textarea',
            plugin = document._front_edit.plugin,
            container,
            editor;


        if (plugin == 'ace') {
            tag = 'div';
        }

        container = $('<'+tag+' class="front-edit-container" id="edit-'+el_id+'"></'+tag+'><p><button class="cancel">cancel</button><button class="save">save</button></p>');

        if(el.is('.editing')) {
            return;
        } else {
            el.addClass('editing');
        }

        el.html(container);

        switch(plugin) {
            case 'ace':
                $.getScript('http://d1n0x3qji82z53.cloudfront.net/src-min-noconflict/ace.js', function(){
                    el.addClass('front-edit-ace');
                    editor = ace.edit("edit-" + el_id);
                    editor.setTheme("ace/theme/monokai");
                    editor.setValue(html);
                    editor.getSession().setMode("ace/mode/html");
                    editor.getSession().setUseWrapMode(true);
                });
                break;
            case 'wymeditor':
                el.find('.front-edit-container').html(html);
                $.getScript(document._front_edit.static_root+'wymeditor/jquery.wymeditor.min.js', function(){
                    el.addClass('front-edit-wym');
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
            default:
                el.find('.front-edit-container').html(html);
                break;
        }

        el.find('.cancel').on('click', function(event) {
            el.html(html);
            el.removeClass('editing');
        });

        el.find('.save').on('click', function(event) {
            var new_html, key = el_id;

            switch(plugin) {
                case 'ace':
                    new_html = editor.getValue();
                    break;
                case 'wymeditor':
                    new_html = $.wymeditors(0).xhtml();
                    break;
                default:
                    new_html = el.find('.front-edit-container').val();
                    break;
            }

            $.post(document._front_edit.save_url, {
                key: key,
                val: new_html,
                csrfmiddlewaretoken: document._front_edit.csrf_token
            }, function(data, textStatus, xhr) {
                // todo: return val
            });
            el.removeClass('editing');
            el.html(new_html);
        });
    });
});
