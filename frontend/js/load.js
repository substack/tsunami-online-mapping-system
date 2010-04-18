google.load("maps", "2");
$(document).ready(function () {
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
        function item (prefix,name,hash) {
            var id = prefix = String(group.get("id"));
            return $(document.createElement("li"))
                .append(
                    $(document.createElement("input"))
                        .attr("type", "checkbox")
                )
                .append(
                    $(document.createElement("label"))
                        .attr("for", id)
                        .append($(document.createTextNode(name)))
                );
        }
        
        var ul = $(document.createElement("ul"));
        markers.each(function (name,marker) {
            if (marker.get("group_id") == group.get("id")) {
                ul.append(item("marker_",name,marker)).hide();
            }
        });
        
        $("ul#markers")
            .append(
                item("group_",name,group)
                    .addClass("collapsable")
                    .toggle(
                        function () {
                            $(this).addClass("expanded");
                            ul.show();
                        },
                        function () {
                            $(this).removeClass("expanded");
                            ul.hide();
                        }
                    )
            )
            .append(ul);
    });
});
