jQuery(document).ready(function($) {
    var editables = $('.editable');

    editables.on('dblclick', function(event) {
        event.preventDefault();

        var el = $(this),
            html = el.html(),
            el_id = el.attr('id'),
            tag = 'textarea',
            container,
            editor;

        if (document._front_edit.plugin == 'ace') {
            tag = 'div';
        }

        container = $('<'+tag+' class="front-edit-container" id="edit-'+el_id+'"></'+tag+'><p><button class="cancel">cancel</button><button class="save">save</button></p>');

        if(el.is('.editing')) {
            return;
        } else {
            el.addClass('editing');
        }

        el.html(container);

        switch(document._front_edit.plugin) {
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

            switch(document._front_edit.plugin) {
                case 'ace':
                    new_html = editor.getValue();
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
