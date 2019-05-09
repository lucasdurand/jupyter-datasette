define(['jquery', 'base/js/utils'], function ($, utils) {

    function reload () {
        // call ?reload on /datasette
        var base_url = utils.get_body_data('baseUrl');
        $.get(`${base_url}/datasette?reload`, success= function(resp){                // refresh iframe
            alert("Now we refresh");
            $("#datasette_iframe").attr('src',$("#datasette_iframe").attr('src'));
        })
    }

    function insert_tab () {
        var tab_text = 'Datasette';
        var tab_id = 'datasette_embed';
        var base_url = utils.get_body_data('baseUrl');

        var datasette_refresh = $('<button/>')
            .text("New Files? Reload Datasette")
            .addClass('btn btn-default')
            .on('click', reload());


        var datasette_ui = $('<iframe/>')
            .attr('id','datasette_iframe')
            .attr('src',`${base_url}/datasette`)
            .attr('style','height:85vh;border:None;')
            .attr('width','100%');

        $('<div/>')
            .attr('id', tab_id)
            .append(datasette_refresh)
            .append(datasette_ui)
            .addClass('tab-pane')
            .appendTo('.tab-content');

        var tab_link = $('<a>')
            .text(tab_text)
            .attr('href', '#' + tab_id)
            .attr('data-toggle', 'tab')
            .on('click', function (evt) {
                window.history.pushState(null, null, '#' + tab_id);
            });

        $('<li>')
            .append(tab_link)
            .appendTo('#tabs');

        // select tab if hash is set appropriately
        if (window.location.hash == '#' + tab_id) {
            tab_link.click();
        }
    }


    var load_ipython_extension = function () {
        insert_tab();
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
