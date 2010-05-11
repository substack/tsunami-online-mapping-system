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
        icon : (this.mutable
            ? new google.maps.Icon(G_DEFAULT_ICON) // default pinkish icon
            : new google.maps.Icon(G_DEFAULT_ICON, "/images/green-marker.png")
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
        .toggle(
            function () { marker.hide() },
            function () { marker.show() }
        )
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
    var maybeDesc = marker.mutable
        ? $("<span>")
        : $("<span>").text(marker.description)
    ;
    
    this.tr = $("<tr>").append(
        $("<td>").append(checkbox),
        $("<td>").append(nameOrBox),
        $("<td>").append(maybeDesc)
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
                gMarker.setLatLng(marker.position);
                
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
        table.css("visibility","visible");
        return this;
    };
    
    this.collapse = function () {
        $(this.elem).removeClass("expanded");
        img.attr("src", "/images/collapsed.png");
        table.css("visibility","hidden");
        return this;
    }
    
    var checkbox = $("<input>").attr({
        name : "group_" + group.name,
        type : "checkbox",
        checked : "false"
    });
    
    var table = $("<table>").attr("id", "group_" + group.id);
    
    $(markers.map(function (i,marker) {
        var row = new MarkerRow(map, new Marker(map,marker));
        return row.tr;
    })).appendTo(table);
    
    var img = $("<img>");
    img.toggle(this.expand,this.collapse);
    
    var label = $("<label>")
        .attr("for", checkbox.attr("name"))
        .text(group.name)
        .toggle(this.expand,this.collapse)
    ;
    
    this.elem = $("<div>").append(img, checkbox, label, table);
}
