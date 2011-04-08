var WideSlideShow = new Class({
    Implements: [Options],

    options:{
        larr: '/static/img/larr.png',
        rarr: '/static/img/rarr.png',
        loader: '/static/img/loader.gif',
        delay: 5000,
    },

    current: 0,
    displayed: null,
    timer: null,

    initialize: function(elem, options, images){
        this.elem = elem;
        this.setOptions(options);
        this.images = images;
        this.addArrows(this.elem);
        this.addLoader(this.elem);
    },

    // images is array of urls
    setImages: function(images){
        this.images = images;
    },

    makeArr: function(name, wrapperCls, arrCls, src){
        var arrWrapper = new Element('div', {
            'class': wrapperCls
        });
        var arr = new Element('img', {
            src: src,
            'class': arrCls
        });
        this[name] = arr;
        return arrWrapper.grab(arr);
    },

    addArrows: function(elem){
        var larrWrapper = this.makeArr('larr', 'arrWrapper larrWrapper', 'arr larr', this.options.larr);
        var rarrWrapper = this.makeArr('rarr', 'arrWrapper rarrWrapper', 'arr rarr', this.options.rarr);

        elem.grab(larrWrapper);
        elem.grab(rarrWrapper);
        this.toggleArrowDisplay(larrWrapper, this.larr, this.rarr);
        this.toggleArrowDisplay(rarrWrapper, this.rarr, this.larr);
        this.initArrClicks(larrWrapper, function(){
            this.next();
        }.bind(this))
        this.initArrClicks(rarrWrapper, function(){
            this.prev();
        }.bind(this))
    },

    toggleArrowDisplay: function(wrapper, arrow, other){
        wrapper.addEvent('mouseover', function(){
            arrow.fade('in');
            other.fade('out');
        })
        wrapper.addEvent('mouseout', function(){
            arrow.fade('out');
        })
    },

    initArrClicks: function(elem, fn){
        elem.addEvent('click', fn);
    },

    addLoader: function(elem){
        this.loader = new Element('img', {
            'src': this.options.loader,
            'styles': {
                'position': 'absolute',
                'left': '50%',
                'top': '50%',
                'opacity': 0
            }
        });
        elem.grab(this.loader);
    },

    toggleLoader: function(){
        this.loader.fade('toggle');
    },

    prepareImage: function(image, styles){
        var width = image.getCoordinates().width;
        image.setStyles(styles);
        return image;
    },

    slideIn: function(image, dir, start, end){
        // if there hasn't been a displayed image
        // just put the image in (don't slide in)
        // and mark it displayed
        var width = image.getCoordinates().width;
        image.set('tween', {
            duration: 800,
            transition: 'quint:in:out',
            link: 'cancel',
            onComplete: function(){
                //this.displayed = image;
            }.bind(this)
        });
        image.tween(dir, start, end);
    },

    slideOut: function(image, dir, start, end){
        var width = image.getCoordinates().width;
        image.set('tween', {
            duration: 800,
            transition: 'quint:in:out',
            link: 'cancel',
            onComplete: function(){
                image.dispose()   
                image.destroy();
            }.bind(this)
        });
        image.tween(dir, start, end);
    },

    slide: function(image, dir, start, end){
        if(this.displayed){
            this.slideIn(image, dir, start, end);

            var temp = start;
            start = end;
            end = -temp;

            this.slideOut(this.displayed, dir, start, end);
        }
        this.displayed = image;
    },

    grab: function(image, styles){
        image.setStyle('visibility','none');
        image.setStyle('position','absolute');
        this.elem.grab(image);
        // if there is already an image, set this
        // one off to the side
        if(this.displayed){
            image = this.prepareImage(image, styles);
        }
        image.setStyle('visibility','visible');
    },

    next: function(){
        var width = this.elem.getCoordinates().width;
        var src = this.images[this.current++ % this.images.length];
        this.change(src,
                    {left: width, top:0},
                    'left',
                    width,
                    0);
    },

    prev: function(){
        var width = this.elem.getCoordinates().width;
        var src = this.images[--this.current % this.images.length];
        this.change(src,
                    {left: 0, top:0},
                    'left',
                    0,
                    width);
    },

    change: function(src, prepare, dir, start, end){
        console.log(arguments);
        this.toggleLoader();
        var image = Asset.image(src, {
            onload: function(){
                this.toggleLoader();
                this.grab(image, prepare);
                this.slide(image, dir, start, end);
                this.timer = this.next.delay(this.options.delay, this); 
            }.bind(this)
        });
    }

/*
    next: function(){
        this.toggleLoader();
        var src = this.images[this.current++ % this.images.length];
        var image = Asset.image(src, {
            onload: function(){
                this.toggleLoader();
                this.grab(image, {
                              left: width,
                              top: 0
                          });
                this.slide(image, tween);
                this.timer = this.next.delay(this.options.delay, this); 
            }.bind(this)
        });
    },

    prev: function(){
        this.toggleLoader();
        var src = this.images[--this.current % this.images.length];
        var image = Asset.image(src, {
            onload: function(){
                this.toggleLoader();
                this.grab(image);
                this.slide(image);
                this.timer = this.next.delay(this.options.delay, this); 
            }.bind(this)
        });
    }
    */

})
