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
        def.overlay = new google.maps.GroundOverlay(
            "/overlays/" + name + ".png",
            new google.maps.LatLngBounds(
                new google.maps.LatLng(def.south,def.east),
                new google.maps.LatLng(def.north,def.west)
            )
        );
        
        $("select#deformations").prepend(
            $("<option>")
                .attr("value", name)
                .text(name)
        );
    });
    
    $("select#deformations").change(function () {
        var name = $(this).attr("value");
        if (name == "") return;
        
        deformations.each(function (_,def) {
            map.removeOverlay(def.overlay)
        });
        map.addOverlay(deformations.at(name).overlay);
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
            return $("<li>")
                .append(
                    $("<input>")
                        .attr("type", "checkbox")
                        .attr("name", name)
                )
                .append(
                    $("<label>")
                        .attr("for", name)
                        .text(name)
                )
            ;
        }
        
        var ul = $("<ul>");
        markers
            .sort() // sort by key name
            .filter(function (name,marker) {
                return marker.group_id == group.id;
            })
            .each(function (name,marker) {
                var li = item("marker_",name,marker);
                li.find("input:checkbox").change(function () {
                    var m = markers.at(name);
                    m.checked = $(this).attr("checked");
                    if (m.checked) {
                        m.marker = new google.maps.Marker(
                            new google.maps.LatLng(m.latitude, m.longitude)
                        );
                        map.addOverlay(m.marker);
                    }
                    else if (m.marker) {
                        map.removeOverlay(m.marker);
                    }
                });
                ul.append(li).hide();
            })
        ;
        
        var im = $("<img>")
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
            ul.find("input:checkbox")
                .attr("checked",checked)
                .change();
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
        var ul = $("<ul>");
        gs.each(function (name,grid) {
            ul.append(
                $("<li>")
                    .append(
                        $("<input>")
                            .attr("type", "checkbox")
                            .attr("name", "grid_" + name)
                            .attr("id", "grid_" + name)
                            .change(function () {
                                if ($(this).attr("checked")) {
                                    map.addOverlay(grid.polygon);
                                    var parent = with_id(grid.parent_id);
                                    console.log(grid.parent_id);
                                    console.log(parent);
                                    if (parent) {
                                        $("#grid_" + parent[1].name)
                                            .attr("checked",true)
                                            .change();
                                    }
                                }
                                else {
                                    map.removeOverlay(grid.polygon);
                                    children(grid).each(function (n,g) {
                                        $("#grid_" + g.name)
                                            .attr("checked",false)
                                            .change();
                                    });
                                }
                            })
                    )
                    .append($("<span>").addClass("grid-name").text(name))
                    .append($("<span>").text(grid.description))
                    .append(gridList(children(grid)))
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
