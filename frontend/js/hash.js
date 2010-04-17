function Hash(elems) {
    if (elems == undefined) elems = {};
    
    this.get = function (key) {
        return elems[key];
    };
    
    this.set = function (key, value) {
        elems[key] = value;
        return this;
    };
    
    this.keys = function () {
        var acc = [];
        for (var key in elems) {
            acc.push(key);
        }
        return acc;
    };
    
    this.values = function () {
        var acc = [];
        for (var key in elems) {
            acc.push(elems[key]);
        }
        return acc;
    };

    this.items = function () {
        var acc = [];
        for (var key in elems) {
            acc.push([ key, elems[key] ]);
        }
        return acc;
    };
    
    this.each = function (f) {
        for (var key in elems) {
            f(key,elems[key]);
        }
        return this;
    };
    
    this.foldl = function (x, f) {
        var acc = x;
        for (var key in elems) {
            acc = f(acc,key,elems[key]);
        }
        return acc;
    };
    
    this.toString = function () {
        function show(x) {
            if (typeof(x) == "string") {
                return '"' + x.replace(/\\/g, '').replace(/"/g, '\\\\') + '"';
            }
            else if (x == null || x == undefined) {
                return String(x);
            }
            else {
                return x.toString();
            }
        }
        return "{" + this.foldl([], function (acc,key,value) {
            acc.push([key,value].map(show).join(":"));
            return acc;
        }).join(",") + "}";
    };
}
