(function(jQuery){
    var triggerEditor = function(el) {
        var body = jQuery('body'),
            front_edit_options = document._front_edit,
            html = el.html(),
            element_id = el.attr('id'),
            container,
            target;

        container = jQuery(
            front_edit_plugin.get_container_html(element_id, front_edit_options) +
                '<p class="front-edit-buttons"><button class="history">history</button><button class="cancel">cancel</button><button class="save">save</button></p>'
        );

        if (body.is('.front-editing')) {
            return;
        }
        body.addClass('front-editing');

        switch(front_edit_options.edit_mode) {
            case 'inline':
                el.html(container);
                target = el;
                break;

            case 'lightbox':
                jQuery('<div id="front-edit-lightbox-container" class="active front-edit-dialog_layer front-edit-layer"><div id="front-edit-lightbox" class="front-edit-dialog"></div></div>').appendTo(jQuery('body'));
                var lightbox = jQuery('#front-edit-lightbox');
                lightbox.html(container);
                target = lightbox;
                break;
        }

        front_edit_plugin.set_html(target, html, front_edit_options);

        target.find('.cancel').on('click', function(event) {
            el.html(html);
            body.removeClass('front-editing');
            front_edit_plugin.destroy_editor();
            jQuery('#front-edit-lightbox-container').remove();
        });

        target.find('.history').on('click', function(event) {
            var btn = jQuery(this);
            jQuery.getJSON(front_edit_options.history_url_prefix + element_id + '/', {}, function(json, textStatus) {
                if (json.history) {
                    var current_val = front_edit_plugin.get_html(front_edit_options);

                    btn.replaceWith(jQuery('<select class="front-edit-history"></select>'));
                    var select = jQuery('.front-edit-history');
                    select.append(
                            jQuery('<option value="0">current edit</option>')
                        );

                    jQuery.each(json.history, function(index, val) {
                        select.append(
                            jQuery('<option value="'+ (index + 1) +'">' + new Date(1000 * parseInt(val.saved, 10)) + '</option>')
                        );
                    });

                    select.on('change', function(event) {
                        var idx = jQuery(this).val();
                        if (idx == 0) {
                            var html = current_val;
                        } else {
                            var html = json.history[idx - 1].value;
                        }
                        front_edit_plugin.set_html(target, html, front_edit_options);
                    });


                } else {
                    btn.replaceWith(jQuery('<span>No history</span>'));
                }
            });
        });


        target.find('.save').on('click', function(event) {
            var key = element_id
                new_html = front_edit_plugin.get_html(front_edit_options);

            jQuery.post(front_edit_options.save_url, {
                key: key,
                val: new_html,
                csrfmiddlewaretoken: front_edit_options.csrf_token
            }, function(data, textStatus, xhr) {
                // todo: return val
            });
            body.removeClass('front-editing');
            el.html(new_html);
            // cleanup callback
            front_edit_plugin.destroy_editor();
            jQuery('#front-edit-lightbox-container').remove();
        });
    };

    jQuery(document).on('dblclick', '.editable', function(event) {
        event.preventDefault();
        var el = jQuery(this);
        triggerEditor(el);
    });
})(jQuery);
