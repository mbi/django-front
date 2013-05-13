jQuery(document).ready(function($) {
    var editables = $('.editable');

    editables.on('dblclick', function(event) {
        event.preventDefault();
        var el = $(this),
            html = el.html(),
            form = $('<textarea>'+html+'</textarea><p><button class="cancel">cancel</button><button class="save">save</button></p>');

        if(el.is('.editing')) {
            return;
        } else {
            el.addClass('editing');
        }

        el.html(form);
        el.find('.cancel').on('click', function(event) {
            el.html(html);
            el.removeClass('editing');
        });
        el.find('.save').on('click', function(event) {
            var new_html = el.find('textarea').val(),
                key = el.attr('id');

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
