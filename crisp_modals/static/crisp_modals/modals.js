(function($){
    $.fn.shake = function(options) {
        let settings = $.extend({
            interval: 100,
            distance: 5,
            times: 4
        }, options );

        $(this).css('position','relative');

        for(let iter=0; iter<(settings.times+1); iter++){
            $(this).animate({ left:((0 === iter%2 ? settings.distance : settings.distance * -1)) }, settings.interval);
        }
        $(this).animate({ left: 0}, settings.interval, function(){});
    };
})(jQuery);


(function ( $ ) {
    $.fn.asyncForm = function (url, options) {
        let target = $(this);
        let defaults = {
            url: url || $(this).data('form-action'),
            setup: function (body) {
                new TomSelect(target, settings);
            },
            complete: function(data) {
                if (data.url) {
                    if (data.modal) {
                        target.load(data.url);
                    } else {
                        window.location.replace(data.url);
                    }
                } else {
                    window.location.reload();
                }
            }
        };
        let settings = $.extend(defaults, options);
        // load form and initialize it
        $.ajax({
            type: 'GET',
            url: settings.url,
            success: function(response) {
                hideModal();
                target.html(response);
                settings.setup(target);
                showModal();
            }
        });
        target.off("click", ":submit");
        target.on("click", ":submit", function(e){
            let form = target.find('form');
            e.preventDefault();
            e.stopPropagation();

            if (!form[0].checkValidity()) {
                form[0].reportValidity();
                return
            }

            let button = $(this);
            button.html('<svg class="spin" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">' +
                '<path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 ' +
                '0 0 1 .192-.41m-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 ' +
                '0 0 0 .534 9"/><path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 ' +
                '0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5 5 0 0 0 8 3M3.1 9a5.002 5.002 ' +
                '0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9z"/></svg>'
            );

            form.ajaxSubmit({
                type: 'post',
                url: form.attr('action'),
                data: {'submit': button.attr('value')},
			    beforeSend: function(xhr, settings){
                    //xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                },
                success: function(data, status, xhr) {
                    let dataType = xhr.getResponseHeader("content-type") || "";
                    // contains form
                    if (/html/.test(dataType)) {
                        let response = $(data);
                        let contents = target.find(".modal-content");
                        let new_contents = response.find('.modal-content');
                        if (contents.length && new_contents.length) {
                            contents.html(new_contents.html());
                            settings.setup(target);
                        } else {
                            hideModal();
                            target.html(data);
                            settings.setup(target);
                            showModal();
                        }
                    } else if (/json/.test(dataType)) {
                        hideModal();
                        settings.complete(data);
                    } else {
                        hideModal();
                    }
                },
                error: function() {
                    button.html('<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">' +
                        '<path d="M6.95.435c.58-.58 1.52-.58 2.1 0l6.515 6.516c.58.58.58 1.519 0 2.098L9.05 ' +
                        '15.565c-.58.58-1.519.58-2.098 0L.435 9.05a1.48 1.48 0 0 1 0-2.098zm1.4.7a.495.495 0 ' +
                        '0 0-.7 0L1.134 7.65a.495.495 0 0 0 0 .7l6.516 6.516a.495.495 0 0 0 .7 ' +
                        '0l6.516-6.516a.495.495 0 0 0 0-.7L8.35 1.134z"/>' +
                        '<path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0M7.1 4.995a.905.905 0 1 1 ' +
                        '1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0z"/></svg>'
                    );
                    button.shake();
                }
            })
        });
    };
}(jQuery));

(function ( $ ) {
    $.fn.loadModal = function (url) {
        let target = $(this);

        // load form and initialize it
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response) {
                hideModal();
                target.html(response);
                showModal();
            }
        });
    };
}(jQuery));


(function ( $ ) {
    $.fn.initModal = function (options = {}) {
        let target = $(this);
        const settings = $.extend({
            attrName: 'data-modal-url'
        }, options);
        $(document).on('click', `[${settings.attrName}]`, function () {
            target.asyncForm($(this).attr(settings.attrName), settings);
        });
        $(document).on('hidden.bs.modal', '.modal', function(){
            target.empty();  // remove contents after hiding
        });
    };
}(jQuery));


function hideModal() {
    let myModalEl = document.getElementById('modal');
    if (myModalEl) {
        let modal = bootstrap.Modal.getInstance(myModalEl);
        modal.hide();
    }
}

function showModal() {
    let my_modal = new bootstrap.Modal('#modal');
    my_modal.show();
    $('#modal').removeAttr('inert');

}