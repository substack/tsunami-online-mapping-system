google.load("maps", "2");
google.load("jquery", "1.4.2");
google.load("jqueryui", "1.8.0");
google.setOnLoadCallback(function () {
    var canvas = $("#map_canvas");
    var map = new google.maps.Map2(canvas.get(0));
    map.setCenter(new google.maps.LatLng(59, -152.1419), 5);
    map.addControl(new google.maps.LargeMapControl());
    map.disableDoubleClickZoom();
    var panel = $("#tabs");
    panel.tabs({ idPrefix : 'tab' });
    
    $(window).resize(function () {
        canvas.height(
            $(window).height()
            - panel.outerHeight()
            - 16
        );
    });
    $(window).resize();
});
