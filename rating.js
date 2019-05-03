$.fn.rates = function() {
    return this.each(function(i,e){$(e).html($('<span/>').width($(e).text()*16));});
};



$('.rates').rates();
