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
    
    deformations.each(function (name,def) {
        $("select#deformations").append(
            $(document.createElement("option"))
                .attr("value", name)
                .text(name)
        );
    });
    
    $("select#deformations").change(function () {
        var name = $(this).attr("value");
        var def = deformations.get(name);
        var wsen = "west south east north".split(" ").map(def.get)
            .map(function (x) {
                while (x > 180) x -= 360;
                while (x < -180) x += 360;
                return x;
            });
        var w = -wsen[0]; var s = wsen[1]; var e = -wsen[2]; var n = wsen[3];
        
        map.clearOverlays();
        map.addOverlay(new google.maps.GroundOverlay(
            "/overlays/" + name + ".png",
            new google.maps.LatLngBounds(
                new google.maps.LatLng(s,w),
                new google.maps.LatLng(n,e)
            )
        ));
    });
});
