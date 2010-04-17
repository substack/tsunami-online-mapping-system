google.load("maps", "2");
google.load("jquery", "1.4.2");
google.load("jqueryui", "1.8.0");
google.setOnLoadCallback(function () {
    var canvas = $("#map_canvas");
    
    // setup the map canvas
    var map = new google.maps.Map2(canvas.get(0));
    map.setCenter(new google.maps.LatLng(59, -152.1419), 5);
    map.addControl(new google.maps.LargeMapControl());
    map.disableDoubleClickZoom();
    
    var tabs = $("#tabs");
    tabs.tabs({ idPrefix : 'tab' });
    
    canvas.resizable({
        handles : 's',
        resize : function (ev,ui) {
            tabs.height($(window).height() - ui.size.height - 30)
        }
    });
    
    $(window).resize(function () {
        canvas.height(
            $(window).height() - tabs.outerHeight() - 10
        );
    });
    $(window).resize();
});
