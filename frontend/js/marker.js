// marker objects
function Marker(map,params) {
    var marker = this; // resolve back to this within nested callbacks
    
    // load param keys into this
    for (var key in params) {
        this[key] = params[key];
    }
    
    this.clone = function () {
        return new Marker(map,this);
    };
    
    var position = new google.maps.LatLng(this.latitude,this.longitude);
    this.gMarker = new google.maps.Marker(position, {
        draggable : true,
        dragCrossMove : true,
        icon : (marker.mutable
            ? new google.maps.Icon(G_DEFAULT_ICON, "/images/green-marker.png")
            : new google.maps.Icon(G_DEFAULT_ICON) // default pinkish icon
        )
    });
    
    this.hide = function () {
        map.removeOverlay(this.gMarker);
        return this;
    };
    
    this.show = function () {
        map.addOverlay(this.gMarker);
        return this;
    };
}

// manage checkboxes for markers
function MarkerRow(map,marker) {
    // the marker's row in the markers tab
    var checkbox = $("<input>")
        .attr("type", "checkbox")
        .attr("name", "marker_" + marker.name)
        .change(function () {
            $(this).attr("checked")
                ? marker.show()
                : marker.hide()
            ;
        })
    ;
    var nameOrBox = marker.mutable
        ? $("<input>")
            .attr("type", "textbox")
            .val(marker.name)
            .change(function () {
                // update the marker input box's name
                var val = $(this).val();
                checkbox.attr("name", "marker_" + val);
                marker.name = val;
            })
        : $("<span>").text(marker.name)
    ;
    var desc = $("<span>").text(marker.description);
    
    this.tr = $("<tr>").append(
        $("<td>").append(checkbox),
        $("<td>").append(nameOrBox),
        $("<td>")
            .css("min-width","5em")
            .append(desc)
    );
    
    this.hide = function () {
        checkbox.attr("checked",false);
        marker.hide();
        return this;
    };
    
    this.show = function () {
        checkbox.attr("checked",true);
        marker.show();
        return this;
    };
    
    if (! marker.mutable) {
        // drag an immutable marker, creating a mutable marker in its place
        google.maps.Event.addListener(
            marker.gMarker, "dragend",
            function (pos) {
                // set the marker back to its old position and hide it
                marker.gMarker.setLatLng(
                    new google.maps.LatLng(
                        marker.latitude, marker.longitude
                    )
                );
                marker.hide();
                
                // add the new marker to the user group
                var row = new MarkerRow(
                    map, new Marker(map,{
                        name : "user_" + marker.name,
                        group_id : -1,
                        latitude : pos.lat(),
                        longitude : pos.lng(),
                        mutable : true,
                    }).show()
                );
                $("table#group_-1").append(row.tr);
            }
        );
    }
}

// collection of markers
function MarkerGroup(map,group,markers) {
    this.expand = function () {
        img.attr("src", "/images/expanded.png");
        table.show();
        return this;
    };
    
    this.collapse = function () {
        img.attr("src", "/images/collapsed.png");
        table.hide();
        return this;
    }
    
    var checkbox = $("<input>")
        .attr({
            name : "group_" + group.name,
            type : "checkbox",
            checked : false
        })
        .change(function () {
            var checked = $(this).attr("checked");
            rows.each(function (i,row) {
                if (checked) row.show();
                else row.hide();
            })
        })
    ;
    
    var table = $("<table>").attr("id", "group_" + group.id);
    var rows = markers.map(function (key,marker) {
        var row = new MarkerRow(map, new Marker(map,marker));
        return row;
    });
    rows.each(function (key,row) {
        table.append(row.tr);
    });
    
    var img = $("<img>");
    img.toggle(this.collapse,this.expand);
    
    var label = $("<label>")
        .attr("for", checkbox.attr("name"))
        .text(group.name)
        .toggle(this.expand,this.collapse)
    ;
    
    var div = $("<div>").append(img, checkbox, label, table);
    this.elem = div;
    this.collapse();
}
