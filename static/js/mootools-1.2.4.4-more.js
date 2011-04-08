//MooTools More, <http://mootools.net/more>. Copyright (c) 2006-2009 Aaron Newton <http://clientcide.com/>, Valerio Proietti <http://mad4milk.net> & the MooTools team <http://mootools.net/developers>, MIT Style License.

MooTools.More={version:"1.2.4.4",build:"6f6057dc645fdb7547689183b2311063bd653ddf"};Fx.Elements=new Class({Extends:Fx.CSS,initialize:function(b,a){this.elements=this.subject=$$(b);
this.parent(a);},compute:function(g,h,j){var c={};for(var d in g){var a=g[d],e=h[d],f=c[d]={};for(var b in a){f[b]=this.parent(a[b],e[b],j);}}return c;
},set:function(b){for(var c in b){var a=b[c];for(var d in a){this.render(this.elements[c],d,a[d],this.options.unit);}}return this;},start:function(c){if(!this.check(c)){return this;
}var h={},j={};for(var d in c){var f=c[d],a=h[d]={},g=j[d]={};for(var b in f){var e=this.prepare(this.elements[d],b,f[b]);a[b]=e.from;g[b]=e.to;}}return this.parent(h,j);
}});
var Asset = {

    javascript: function(source, properties){
        if (!properties) properties = {};

        var script = new Element('script', {src: source, type: 'text/javascript'}),
            doc = properties.document || document,
            loaded = 0,
            loadEvent = properties.onload || properties.onLoad;

        var load = loadEvent ? function(){ // make sure we only call the event once
            if (++loaded == 1) loadEvent.call(this);
        } : function(){};

        delete properties.onload;
        delete properties.onLoad;
        delete properties.document;

        return script.addEvents({
            load: load,
            readystatechange: function(){
                if (['loaded', 'complete'].contains(this.readyState)) load.call(this);
            }
        }).set(properties).inject(doc.head);
    },

    css: function(source, properties){
        if (!properties) properties = {};

        var link = new Element('link', {
            rel: 'stylesheet',
            media: 'screen',
            type: 'text/css',
            href: source
        });

        var load = properties.onload || properties.onLoad,
            doc = properties.document || document;

        delete properties.onload;
        delete properties.onLoad;
        delete properties.document;

        if (load) link.addEvent('load', load);
        return link.set(properties).inject(doc.head);
    },

    image: function(source, properties){
        if (!properties) properties = {};

        var image = new Image(),
            element = document.id(image) || new Element('img');

        ['load', 'abort', 'error'].each(function(name){
            var type = 'on' + name,
                cap = 'on' + name.capitalize(),
                event = properties[type] || properties[cap] || function(){};

            delete properties[cap];
            delete properties[type];

            image[type] = function(){
                if (!image) return;
                if (!element.parentNode){
                    element.width = image.width;
                    element.height = image.height;
                }
                image = image.onload = image.onabort = image.onerror = null;
                event.delay(1, element, element);
                element.fireEvent(name, element, 1);
            };
        });

        image.src = element.src = source;
        if (image && image.complete) image.onload.delay(1);
        return element.set(properties);
    },

    images: function(sources, options){
        sources = Array.from(sources);

        var fn = function(){},
            counter = 0;

        options = Object.merge({
            onComplete: fn,
            onProgress: fn,
            onError: fn,
            properties: {}
        }, options);

        return new Elements(sources.map(function(source, index){
            return Asset.image(source, Object.append(options.properties, {
                onload: function(){
                    counter++;
                    options.onProgress.call(this, counter, index, source);
                    if (counter == sources.length) options.onComplete();
                },
                onerror: function(){
                    counter++;
                    options.onError.call(this, counter, index, source);
                    if (counter == sources.length) options.onComplete();
                }
            }));
        }));
    }

};
