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
            tabs.height($(window).height() - ui.size.height - 30);
            $("#markers-tab").height(
                tabs.height() - $("#tabs-bar").height()
            );
        }
    });
    
    tabs.height($(window).height() - canvas.height - 30);
    $("#markers-tab").height(
        tabs.height() - $("#tabs-bar").height() - 15
    );
    
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
        map.clearOverlays();
        
        var name = $(this).attr("value");
        if (name == "") return;
        
        var def = deformations.get(name);
        var w = def.get("west");
        var s = def.get("south");
        var e = def.get("east");
        var n = def.get("north");
        
        map.addOverlay(new google.maps.GroundOverlay(
            "/overlays/" + name + ".png",
            new google.maps.LatLngBounds(
                new google.maps.LatLng(s,e),
                new google.maps.LatLng(n,w)
            )
        ));
    });
    
    groups.each(function (name,group) {
        $("#markers-tab").append(
            $(document.createElement("div"))
                .addClass("marker")
                .append($(document.createElement("input"))
                    .attr("type", "checkbox")
                    .attr("value", name)
                )
                .append($(document.createTextNode(name)))
            )
        ;
    });
});
