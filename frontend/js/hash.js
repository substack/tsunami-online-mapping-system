function Hash(items) {
    if (items == undefined) items = {};
    if (items instanceof Hash) {
        items = items.items;
    }
    this.__items__ = items;
    
    this.foldr = function (f,acc) {
        for (var key in this.__items__) {
            acc = f(key,this.__items__[key],acc);
        }
        return acc;
    };
    
    this.foldl = function (f,acc) {
        return this.foldr(function (key,value,acc) {
            return f(acc,key,value);
        }, acc);
    };
    
    this.map = function (f) {
        return this.foldl(function (acc,key,value) {
            return acc.cons(key,f(key,value));
        }, new Hash());
    };
    
    this.filter = function (f) {
        return this.foldl(function (acc,key,value) {
            if (f(key,value)) {
                return acc.cons(key,value);
            }
            else {
                return acc;
            }
        }, new Hash());
    };
    
    this.each = function (f) {
        for (var key in this.__items__) {
            f(key, this.__items__[key]);
        }
        return undefined;
    };
    
    this.concat = function (that) {
        return that.foldl(function (hash,key,value) {
            return hash.cons(key,value);
        }, new Hash(this));
    };
    
    this.cons = function (key,value) {
        var elems = this.items;
        elems[key] = value;
        return new Hash(elems);
    };
    
    this.at = function (key,value) {
        return this.__items__[value];
    };
    
    this.sort = function (f) {
        return this.pairs.sort().reduce(function (hash,pair) {
            return hash.cons(pair[0], pair[1]);
        }, new Hash());
    };
    
}

Hash.prototype = {
    get pairs () {
        return this.foldl(function (acc,key,value) {
            return acc.concat([[key,value]]);
        }, []);
    },
    get items () {
        return this.foldl(function (acc,key,value) {
            acc[key] = value;
            return acc;
        }, {})
    },
    get keys () {
        return this.foldl(function (acc,key,_) {
            return acc.concat([key]);
        }, [])
    },
    get values () {
        return this.foldl(function (acc,_,value) {
            return acc.concat([value]);
        }, [])
    },
};
