var echbNS = echbNS || {};

echbNS.UI = function (core) {
    var showClosestChurches = function () {

        $('#closest-churches-list').empty();

        closestChurches = core.getClosestChurches(6);
        closestChurches.forEach(churchOnMap => {
            church = churches.filter(ch => ch.pk == churchOnMap.churchId)[0].fields;
            church.distance = Math.round(churchOnMap.distance);
            content = tmpl("church-info-search", church);
            $('#closest-churches-list').append(content);
        });

        core.filterMarkers(core.filterByClosestChurches);

        core.addUserPositionToMap();
        
        return false;
    };

    var showRegionsInMenu = function () {
        $('#regions').append('<li><a href="" data-val-region="0">Все</a></li>');
        regions.forEach(region => {
            $('#regions').append('<li><a href="" data-val-region=' + region.pk + '>' + region.fields.name + '</a></li>');
        });
    };

    var initializeEventsOnDom = function () {
        $(document)
            .on('click', 'a#closestChurches', showClosestChurches)
            .on('click', 'a.church-details', function (e) {
                if ( $(this).next().next().css('display') == 'none') {
                    $(this).next().next().show();
                } else {
                    $(this).next().next().hide();
                }
                return false;
            })
            .on('click', 'a.church-route', function (e) {
                core.calculateRoute($(this).attr('data-val-lat'), $(this).attr('data-val-lng'));
                return false;
            });

        $('#regions').on('click', 'li a', function (e) {
            $('.active-region').removeClass('active-region');
            $(this).addClass('active-region');
            core.filterMarkers(core.filterByRegion, options = $(this).attr('data-val-region'));
            return false;
        });
    };
    var initialize = function () {
        core.initializeMap(49.8353139, 36.663565, 8, 'map');
        core.addChurchMarkersToMap();
        showRegionsInMenu();
        initializeEventsOnDom();
    };
    return {
        initialize: initialize
    };
};