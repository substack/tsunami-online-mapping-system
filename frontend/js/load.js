google.load("maps", "2");
var moo;
$(document).ready(function () {
    var canvas = $("#map_canvas");
    
    // setup the map canvas
    var map = new google.maps.Map2(canvas.get(0));
    map.setCenter(new google.maps.LatLng(59, -152.1419), 5);
    map.addControl(new google.maps.LargeMapControl());
    map.addControl(new google.maps.MenuMapTypeControl());
    
    //map.disableDoubleClickZoom();
    map.addMapType(G_SATELLITE_MAP);
    map.setMapType(G_SATELLITE_MAP);
    
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
    
    groups.each(function (acc,group) {
        var mGroup = new MarkerGroup(
            map, group,
            markers.filter(function (key,marker) {
                return marker.group_id == group.id;
            })
        );
        $("div#marker-groups").append(mGroup.elem);
    });
    
    $("img#marker").draggable({ helper : "clone" });
    canvas.droppable({
        drop : function (ev,ui) {
            var pt = map.fromContainerPixelToLatLng(
                new google.maps.Point(
                    ev.pageX - ev.offsetX + 8,
                    ev.pageY - ev.offsetY + 33
                )
            );
            
            var row = new MarkerRow(
                map, new Marker(map, {
                    name : [0,0,0,0].map(function () {
                            return String(Math.floor(Math.random()*10));
                        }).join(""),
                    mutable : true,
                    group_id : -1,
                    latitude : pt.lat(),
                    longitude : pt.lng(),
                }).show()
            );
            $("table#group_-1").append(row.tr);
        }
    });
    
    $.getJSON("/data/priority-lists/get", function (data) {
        $(data).map(function (i,x) {
            var overlay = new GGeoXml(x.kml);
            return $("<p>")
                .text(x.name)
                .append($("<input>")
                    .attr("type","checkbox")
                    .change(function () {
                        if ($(this).attr("checked")) {
                            map.addOverlay(overlay);
                        }
                        else {
                            map.removeOverlay(overlay);
                        }
                    })
                )
            ;
        }).appendTo($("#priority-lists"));
    });
    
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
    
    drawGrids(map);
    updateJobs();
});

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
    
    grids.sort().each(function (name,grid) {
        grid.polygon = new google.maps.Polygon(
            [ // latlngs
                new google.maps.LatLng(grid.north, grid.west),
                new google.maps.LatLng(grid.north, grid.east),
                new google.maps.LatLng(grid.south, grid.east),
                new google.maps.LatLng(grid.south, grid.west),
                new google.maps.LatLng(grid.north, grid.west)
            ],
            "red", 2, 0.6, // stroke color, weight, opacity
            "red", 0.08 // fill color, opacity
        );
        
        grid.coastline = new google.maps.GeoXml(
            "http://burn.giseis.alaska.edu/grids/" + name + ".kml"
        );
         
        $("select#coastline").prepend(
            $("<option>").val(name).text(name)
        );
    });
    
    $("select#coastline").prepend(
        $("<option>").val("").text("")
    );
    
    function gridList(gs) {
        var ul = $("<ul>");
        gs.each(function (name,grid) {
            ul.append($("<li>").append(
                $("<input>")
                    .attr("type", "checkbox")
                    .attr("name", "grid_" + name)
                    .attr("id", "grid_" + name)
                    .change(function () {
                        if ($(this).attr("checked")) {
                            map.addOverlay(grid.polygon);
                            var parent = with_id(grid.parent_id);
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
                ,
                $("<span>").addClass("grid-name").text(name),
                $("<span>").text(grid.description),
                gridList(children(grid))
            ));
        });
        return ul;
    }
    
    $("#grids-tab").append(gridList(
        grids.filter(function (name,grid) { // top-level grids
            return grid.parent_id == null;
        })
    ).attr("id", "grids"));
    
    $("select#coastline").change(function () {
        grids.each(function (i,g) {
            map.removeOverlay(g.coastline);
        });
        
        if ($(this).val().length) {
            var grid = grids.at($(this).val())
            map.addOverlay(grid.coastline);
        }
    });
}

function updateJobs() {
    function drawStatus(status,jobs,buttons) {
        var rows = $(jobs)
            .filter(function (i,job) {
                return job.status == status;
            })
            .map(function (i,job) {
                var row = $("<tr>").append(
                    $("<td>").text(job.id),
                    $("<td>").text(job.name)
                );
                $(buttons).map(function (i,button) {
                    return $("<input>")
                        .attr("type","button")
                        .val(button.value)
                        .click(function () {
                            $.get(
                                "/data/jobs/" + button.value + "/" + job.id,
                                function (data) {
                                    if (data == "ok") {
                                        if (button.value == "remove") row.remove();
                                    }
                                    else alert(data);
                                }
                            );
                        })
                    ;
                }).appendTo(row.find("td:last"));
                return row;
            })
        ;
        
        if (rows.size()) {
            $("table#jobs").append(
                $("<tr>").append(
                    $("<th>")
                        .addClass("job-status-row")
                        .attr("colspan",2)
                        .text(status)
                ),
                $("<tr>").append(
                    $("<th>")
                        .css("width", "4em")
                        .text("id"),
                    $("<th>").text("name")
                )
            );
            rows.appendTo("table#jobs");
        }
    }
    
    $.getJSON('/data/jobs/get', function (jobs) {
        $("table#jobs").empty();
        
        drawStatus("pending",jobs, [
            { value : "remove" }
        ]);
        drawStatus("starting",jobs, [
            { value : "stop" },
            { value : "remove" }
        ]);
        drawStatus("stopping",jobs, [
            { value : "stop" },
            { value : "remove" }
        ]);
        drawStatus("running",jobs, [
            { value : "stop" }
        ]);
        drawStatus("stopped",jobs, [
            { value : "start" },
            { value : "remove" }
        ]);
        drawStatus("finished",jobs, [
            { value : "archive" },
            { value : "remove" }
        ]);
        drawStatus("archiving",jobs);
        drawStatus("archived",jobs, [
            { value : "unarchive" }
        ]);
        
        setTimeout(updateJobs, 10 * 1000); // check again after 10 seconds
    });
}
