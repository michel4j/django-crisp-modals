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
    $.fn.asyncForm = function (options) {
        let target = $(this);
        let defaults = {
            url: $(this).data('form-action'),
            setup: function (body) {
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
                target.html(response);
                settings.setup(target);
                let my_modal = new bootstrap.Modal('#modal', {backdrop: 'static'});
                my_modal.show();
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
            button.html('<i class="ti ti-reload spin"></i>');

            form.ajaxSubmit({
                type: 'post',
                url: form.attr('action'),
                data: {'submit': button.attr('value')},
			    beforeSend: function(xhr, settings){
                    // xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
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
                            target.html(data);
                            settings.setup(target);
                            let my_modal = new bootstrap.Modal('#modal', {backdrop: 'static'});
                            my_modal.show();
                        }
                    } else if (/json/.test(dataType)) {
                        let my_modal = document.getElementById('#modal');
                        my_modal.hide();
                        settings.complete(data);
                    } else {
                        let my_modal = document.getElementById('#modal');
                        my_modal.hide();
                    }
                },
                error: function() {
                    button.html('<i class="bi-exclamation-diamond"></i>');
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
                target.html(response);
                let my_modal = new bootstrap.Modal('#modal', {backdrop: 'static'});
                my_modal.show();
            }
        });
    };
}(jQuery));


(function ( $ ) {
    $.fn.initModal = function () {
        let target = $(this);
        $(document).on('click', '[data-modal-url]', function () {
            target.asyncForm({url: $(this).data('modal-url')});
        });
        $(document).on('hidden.bs.modal', '.modal', function(){
            target.empty();  // remove contents after hiding
        });
    };
}(jQuery));
