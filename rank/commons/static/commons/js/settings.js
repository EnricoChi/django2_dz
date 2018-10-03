$(document).ready(function () {
    let form = $('#for-cart-items');
    let button = $('.for-cart-items-button');

    button.on('click', function () {
        let company_id = $(this).attr('data-company-id');

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: {
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                'company_id': company_id
            },
            success: function (response) {
                if (response['success']) {

                    let resp_block = $('#for-company-' + company_id);

                    resp_block
                        .siblings('button')
                        .removeClass('col-12')
                        .addClass('col-8');

                    resp_block
                        .html('<i style="font-size: 18px;" class="icon ion-archive mr-1" aria-hidden="true"></i> ' + response['success']['count'])
                        .removeClass('d-none')
                        .addClass('d-inline');
                }
            },
            error: function (response) {

            }
        });

        return false;
    });
});