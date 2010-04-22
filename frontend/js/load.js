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
        
        var def = deformations.at(name);
        var w = def.at("west");
        var s = def.at("south");
        var e = def.at("east");
        var n = def.at("north");
        
        map.addOverlay(new google.maps.GroundOverlay(
            "/overlays/" + name + ".png",
            new google.maps.LatLngBounds(
                new google.maps.LatLng(s,e),
                new google.maps.LatLng(n,w)
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
        
        $("ul#markers")
            .append(elem)
            .append(ul)
        ;
    });
});
