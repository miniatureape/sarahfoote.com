function fit(item, container){
        var ic = item.getCoordinates();
        var cc = container.getCoordinates();
        var diff = {};
        diff['width'] = cc.width - ic.width;
        diff['height'] = cc.height - ic.height;
        // if element is smaller, just return
        if(diff['width'] > 0 && diff[height] > 0) return;

        var props = ["height", "width"];
        if(diff['width'] > diff['height']){
            props.reverse()
        }
        var ratio = cc[props[0]] / ic[props[0]];
        if(ic[props[0]] > cc[props[0]]){
            item.set(props[0], cc[props[0]]);
            item.set(props[1], (ratio) * ic[props[1]]);
        }
    }
window.addEvent('domready', function(){
        var slideshowImgs = document.id('item-slideshow').getElements('img');
        slideshowImgs.each(function(item){
              fit(item, document.id('item-slideshow'));
        });
        var slideshow = new SlideShow('item-slideshow');
        slideshow.play();
});
