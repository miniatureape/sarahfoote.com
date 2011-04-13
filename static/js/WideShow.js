var WideSlideShow = new Class({
    Implements: [Options],

    options:{
        larr: '',
        rarr: '',
        loader: '/static/img/loader.gif',
        delay: 5000
    },

    current: 0,
    displayed: null,
    timer: null,

    initialize: function(elem, options, images){
        this.elem = elem;

        // temp
        this.elem.addEvent('click', function(){
            clearTimeout(this.timer);
            this.next();
        }.bind(this));
        this.setOptions(options);
        this.images = images;
        this.addArrows(this.elem);
        this.addLoader(this.elem);
    },

    // images is array of urls
    setImages: function(images){
        this.images = images;
    },
    addArrows: function(elem){
        var larr = new Element('img', {
            src: this.options.larr,
            styles: {
                'position': 'absolute',
                'top': '50%',
                'left': '0',
                'opacity': 0
            },
        });

        var rarr = larr.clone();
        rarr.setStyle('left', 'auto');
        rarr.setStyle('right', '0');

        elem.grab(larr);
        elem.grab(rarr);
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

    prepareImage: function(image){
        var width = image.getCoordinates().width;
        image.setStyles({
            left: width,
            top: 0
        });
        return image;
    },

    slideIn: function(image){
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
        image.tween('left', width, 0);
    },

    slideOut: function(image){
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
        image.tween('left', 0, -width);
    },

    slide: function(image){
        if(this.displayed){
            this.slideIn(image);
            this.slideOut(this.displayed);
        }
        this.displayed = image;
    },

    grab: function(image){
        image.setStyle('visibility','none');
        image.setStyle('position','absolute');
        this.elem.grab(image);
        // if there is already an image, set this
        // one off to the side
        if(this.displayed){
            image = this.prepareImage(image);
        }
        image.setStyle('visibility','visible');
    },

    next: function(){
        this.toggleLoader();
        var src = this.images[this.current++ % this.images.length];
        var image = Asset.image(src, {
            onload: function(){
                this.toggleLoader();
                this.grab(image);
                this.slide(image);
                this.timer = this.next.delay(this.options.delay, this); 
            }.bind(this)
        });
    }

})
