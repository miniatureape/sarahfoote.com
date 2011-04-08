window.startSlideshow = function(images){
    $$('.slideshow').each(function(item){
        var ss = new WideSlideShow(item);
        ss.setImages(images);
        ss.next();
    })
}

window.addEvent('domready', function(){
    var options = {};
    var req = new Request.JSON({
        url: '/slideshow/get_images',
        onSuccess: startSlideshow
    });
    req.get();
    var images = []; // get image urls
});
