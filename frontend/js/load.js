google.load("maps", "2");
var moo;
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
        
        var def = deformations.at(name);
        map.addOverlay(new google.maps.GroundOverlay(
            "/overlays/" + name + ".png",
            new google.maps.LatLngBounds(
                new google.maps.LatLng(def.south,def.east),
                new google.maps.LatLng(def.north,def.west)
            )
        ));
    });
    
    groups.each(function (name,group) {
        function item (prefix,name,hash,collapse) {
            return $(document.createElement("li"))
                .append(
                    $(document.createElement("input"))
                        .attr("type", "checkbox")
                        .attr("name", name)
                )
                .append(
                    $(document.createElement("label"))
                        .attr("for", name)
                        .append($(document.createTextNode(name)))
                )
            ;
        }
        
        var ul = $(document.createElement("ul"));
        markers
            .sort() // sort by key name
            .filter(function (name,marker) {
                return marker.group_id == group.id;
            })
            .each(function (name,marker) {
                ul.append(item("marker_",name,marker)).hide();
            })
        ;
        
        var im = $(document.createElement("img"))
            .attr("src", "/images/collapsed.png")
            .toggle(expand,collapse);
        
        function expand () {
            im.attr("src", "/images/expanded.png");
            ul.show();
        }
        
        function collapse () {
            $(elem).removeClass("expanded");
            im.attr("src", "/images/collapsed.png");
            ul.hide();
        }
        
        var elem = item("group_",name,group)
            .addClass("collapsable")
            .prepend(im)
        ;
        elem.find("input:checkbox").change(function () {
            var checked = $(this).attr("checked");
            ul.find("input:checkbox").attr("checked",checked);
        });
        
        elem.find("label").toggle(expand,collapse);
        
        $("ul#markers")
            .append(elem)
            .append(ul)
        ;
        
        $("img#marker").draggable({ helper : "clone" });
        canvas.droppable({
            drop : function (ev,ui) {
                var pt = map.fromContainerPixelToLatLng(
                    new google.maps.Point(
                        ev.pageX - ev.offsetX + 8,
                        ev.pageY - ev.offsetY + 33
                    )
                );
                var name = $("#new-marker-name").val();
                markers = markers.cons(name, {
                    name : name,
                    latitude : pt.lat(),
                    longitude : pt.lng(),
                    mutable : true,
                });
                map.addOverlay(new google.maps.Marker(pt), {
                    dragCrossMove : true
                });
            }
        });
    });
});
