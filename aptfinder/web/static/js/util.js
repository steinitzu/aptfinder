function sort_by_key(array, key, reverse) {
    return array.sort(function(a, b) {
        var x = a[key]; var y = b[key];
        if (reverse) {
            return ((x > y) ? -1 : ((x < y) ? 1 : 0));
        } else {
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        };

    });
};


function EncodeQueryData(data)
{
   var ret = [];
   for (var d in data)
      ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
   return ret.join("&");
};
