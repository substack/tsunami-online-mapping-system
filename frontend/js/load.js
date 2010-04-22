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
            $(".tab").height(
                tabs.height() - $("#tabs-bar").height()
            );
        }
    });
    
    tabs.height($(window).height() - canvas.height - 30);
    $(".tab").height(
        tabs.height() - $("#tabs-bar").height() - 15
    );
    
    $(window).resize(function () {
        canvas.height(
            $(window).height() - tabs.outerHeight() - 10
        );
    });
    $(window).resize();
    
    deformations.each(function (name,def) {
        $("select#deformations").prepend(
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
    drawMarkers(map);
    drawGrids(map);
});

function drawMarkers(map) {
    markers.filter(function (x) { return x.marker }).each(function (x) {
        map.removeOverlay(x.marker);
    });
    
    groups.cons("User", { id : -1, name : "User" }).each(function (name,group) {
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
                var li = item("marker_",name,marker);
                li.find("input:checkbox").change(function () {
                    console.log($(this).attr("checked"));
                    var c = $(this).attr("checked");
                    var m = markers.at(name);
                    m.checked = c;
                    if (c && !m.marker) {
                        m.marker = new google.maps.Marker(
                            new google.maps.LatLng(m.latitude, m.longitude)
                        );
                        map.addOverlay(m.marker);
                    }
                });
                ul.append(li).hide();
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
        var canvas = $("#map_canvas");
        canvas.droppable({
            drop : function (ev,ui) {
                var pt = map.fromContainerPixelToLatLng(
                    new google.maps.Point(
                        ev.pageX - ev.offsetX + 8,
                        ev.pageY - ev.offsetY + 33
                    )
                );
                var name = $("#new-marker-name").val();
                var marker = {
                    name : name,
                    checked : true,
                    group_id : -1,
                    latitude : pt.lat(),
                    longitude : pt.lng(),
                    mutable : true,
                    marker : new google.maps.Marker(pt, {
                        draggable : true,
                        dragCrossMove : true
                    })
                };
                markers = markers.cons(name, marker);
                map.addOverlay(marker.marker);
                $("ul#markers").empty();
                drawMarkers(map);
            }
        });
    });
}

function drawGrids(map) {
    function with_id (id) {
        return grids.first(function (key,grid) {
            return grid.id == id;
        });
    }
    
    function children (grid) {
        return grids.filter(function (key,g) {
            return g.parent_id == grid.id;
        });
    }
    
    grids.each(function (name,grid) {
        grid.polygon = new google.maps.Polygon([
            new google.maps.LatLng(grid.north, grid.west),
            new google.maps.LatLng(grid.north, grid.east),
            new google.maps.LatLng(grid.south, grid.east),
            new google.maps.LatLng(grid.south, grid.west),
            new google.maps.LatLng(grid.north, grid.west)
        ]);
    });
    
    function gridList(gs) {
        var ul = $(document.createElement("ul"));
        gs.each(function (name,grid) {
            function change() {
                if ($(this).attr("checked")) {
                    var pair = with_id(grid.parent_id);
                    while (pair != undefined) {
                        var parent = pair[1];
                        $("#grid_" + parent.name).attr("checked",true);
                        pair = with_id(parent.parent_id);
                    }
                }
            }
            
            ul.append(
                $(document.createElement("li"))
                    .append(
                        $(document.createElement("input"))
                            .attr("type", "checkbox")
                            .attr("name", "grid_" + name)
                            .attr("id", "grid_" + name)
                            .change(change)
                    )
                    .append(
                        $(document.createElement("span"))
                            .append($(document.createTextNode(name)))
                    )
                    .append(
                        $(document.createTextNode(grid.description))
                    )
                    .append(
                        gridList(children(grid))
                    )
            );
        });
        return ul;
    }
    
    $("#grids-tab").append(gridList(
        grids.filter(function (name,grid) { // top-level grids
            return grid.parent_id == null;
        })
    ).attr("id", "grids"));
}
