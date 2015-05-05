jQuery(document).ready(function() {

	var ie7 = (jQuery.browser.msie && jQuery.browser.version.substring(0, 2) == "7.") ? true : false
	var ie8 = (jQuery.browser.msie && jQuery.browser.version.substring(0, 2) == "8.") ? true : false

	// CSS3 fixes for old browsers
	if(ie7 || ie8){
		jQuery("ul.features li:nth-child(3n)").each(function(){ jQuery(this).css("margin-right","0"); })
		jQuery("ul.polaroids li.polaroid").css({"float":"left","border":"1px solid #cccccc","margin-right":"14px"});
		jQuery("ul.polaroids li.polaroid:nth-child(6n)").css("margin-right","-2px");
		jQuery(".clearfix").after("<div style=\"clear:both;\"> </div>");
		jQuery('body').append("<style type=\"text/css\">#main { border-left: 1px solid #cccccc; border-right: 1px solid #cccccc; }");
	}

	// Feature carousel
	if(jQuery("body.front ul.features").length > 0){
		var feat = jQuery("body.front ul.features");
		feat.css({"position":"relative"});
		var li = feat.find("li");
		var h = li.outerHeight();
		var wide = li.outerWidth()+16;
		li.css({"margin-right":"16px"});
		var o = feat.offset();
		var p = feat.position();
		var w = feat.outerWidth();
		var offset = 0;
		var isAnimating = false;
		var timer;
		if(ie7) jQuery("body.front .view-id-features_list").css({"position":"relative"});
		jQuery('body').append("<style type=\"text/css\"> .featurenav { position:absolute;width:32px;height:113px;z-index:10;cursor:pointer; } .featurenav:hover { background-color: rgba(0,0,0,0.5); } @media (max-width: 1024px), (max-device-width: 1024px) { .featurenav { display: none; } ul.features { width: 100%; } body.front .view-features-list { height: auto!important; } ul.features li { width: 46%; max-width: 100%; margin-bottom: 16px; } ul.features li:nth-child(3n) { margin-right: 16px!important; } } @media (max-width: 630px), (max-device-width: 630px) { ul.features li { width: auto; max-width: 100%; } }</style>");
		var l = "<div style=\"left:0px;top:0px;\" class=\"featurenav featurenav-left\"><img src=\"/sites/default/modules/lco_slideshow/images/leftbar_s.png\" alt=\"Previous features\" /></div>";
		var r = "<div style=\"right:0px;top:0px;\" class=\"featurenav featurenav-right\"><img src=\"/sites/default/modules/lco_slideshow/images/rightbar_s.png\" alt=\"More features\" /></div>";
		if(ie7) jQuery("body.front .rowlast").prepend(l).append(r);
		else feat.before(l).after(r);
		
		function shiftFeature(dx){
			var s = (dx > 0) ? "+=" : "-=";
			feat.animate({"left":s+16},200);
			offset = dx*16;
		}
		function setFullWidth(){
			var li = jQuery("body.front ul.features").find("li");
			var wide = li.length*(li.outerWidth()+16);
			if(jQuery('body.front .rowlast').outerWidth() == 976) jQuery("body.front ul.features").css({"width":wide+"px"});
			else jQuery("body.front ul.features").css({"width":"auto"});
		}
		function scrollFeature(d,delay){
			if(isAnimating) return;
			if(jQuery('body').outerWidth() < 1024) return;
			setFullWidth();
			if(!d) d = -1;
			if(!delay) delay = 1000;
			isAnimating = true;
			var s = (d > 0) ? "+=" : "-=";
			var o = feat.position();
			dx = wide*3;
			if(d > 0){
				if(o.left+dx > 0){
					feat.css({"left":"-"+(dx-offset)+"px"}).append(li.slice(0,-3).detach());
					li = feat.find("li");
				}
			}else{
				if(o.left-dx+li.length*wide <= dx){
					feat.append(li.slice(0,3).detach()).css({"left":(o.left+dx-16)+"px"});
					li = feat.find("li");
				}
			}
			feat.animate({"left":s+(dx)},delay,function(){ isAnimating = false; })
		}

		setFullWidth();
		jQuery(".featurenav-left").click(function(){ scrollFeature(1) }).mouseover(function(){ clearInterval(timer); shiftFeature(1) } ).mouseout(function(){ shiftFeature(-1) } );
		jQuery(".featurenav-right").click(function(){ scrollFeature(-1) }).mouseover(function(){ clearInterval(timer); shiftFeature(-1) } ).mouseout(function(){ shiftFeature(1) } );
		jQuery(window).resize(function(e){
			setFullWidth();
		});
		timer = setInterval(function(){ scrollFeature(-1,2000) },10000);
	}

	// Load an observation block
	if(jQuery("#observations").length > 0){
		ncol = 5; //jQuery("#observations")
		nrow = 4;
		jQuery.ajax({
			url: "http://lcogt.net/observations/recent.json",
			dataType: "jsonp",
			success: function(data){
				obs = data.observation
				if(obs.length == 10)
					for(var i = 0; i < 10 ; i++) obs.push(obs[i])
				o = "";
				for(var i = 0 ; i < ncol*nrow ; i++){
					mr = (i % ncol == ncol-1) ? 0 : 1;
					mb = (i < (ncol*(nrow-1))) ? 1 : 0;
					o += "<a href=\""+obs[i].about+"\"><img src=\""+obs[i].image.thumb+"\" alt=\""+obs[i].image.label+"\" title=\""+obs[i].label+"\" style=\"margin-right:"+mr+"px;margin-bottom:"+mb+"px;float:left;width:60px;height:60px;\" \/><\/a>";
				}
				jQuery("#observations").html(o)
				if(jQuery("#observations img").length > 0) imageLoadError("#observations img");
			}
		});
	}

	// Side image links - a fix because Drupal doesn't do it properly
	jQuery(".field-type-media .small_thumbnail_sq").each(function(){
		if(jQuery(this).find("a").length==0){
			loc = jQuery(this).find("img").attr("src").replace(/styles\/small_thumbnail_sq\/public\//,'');
			jQuery(this).replaceWith("<a href=\""+loc+"\">"+jQuery(this).html()+"</a>");
		}
	})

	// Make image captions from the title text
	jQuery('img.image-caption').each(function(){
		i = jQuery(this);
		title = i.attr('title');
		if(title){
			align = i.css('float');
			w = (i.width() > 0) ? 'width:'+i.width()+'px;' : '';
			if(align) i.css({'float':'none','margin':'0px','margin-bottom':'4px'});
			margin = (align=="left") ? "margin-right:16px;" : (align=="right" ? "margin-left:16px;" : "");
			el = (jQuery(this).parent().attr("tagName").toLowerCase()!="a") ? i : i.parent();	
			el.wrap('<div style="text-align:center;color:#606060;font-size:0.9em;'+w+(align ? 'float:'+align+';'+margin+'margin-bottom:16px;' : "")+'">').after('<br />'+title);
			if(w <= 0){
				i.load({el:el},function(e){ e.data.el.parent().css('width',jQuery(this).width()); });
			}
		}
	});

	function imageLoadError(el,sz){
		jQuery(el).each(function(){
				var missing = (jQuery(this).outerWidth() > 200) ? "/sites/default/themes/lcogt/images/missing_large.png" : "/sites/default/themes/lcogt/images/missing.png";
				// Work	around for error function reporting of file load failure
				this.src = this.src;
				jQuery(this).bind("error",function() {
					this.src = missing;
					this.alt = "Image unavailable";
					this.onerror = "";
					return true;
				})
		});
	}

	// Add a lightbox to "media-image" class images
	jQuery('img.media-image').each(function(){
		// Check if the immediate parent is a link. If it isn't we will make it one.
		linkify = false;
		el = jQuery(this);
		if(el.parent().attr("tagName").toLowerCase()!="a"){
			linkify = true;
			if(el.parent().attr("tagName").toLowerCase()=="span" && el.parent().parent().attr("tagName").toLowerCase()=="a"){
				linkify = false;
				el = el.parent().parent();
			}
			if(linkify){
				// Parse out the extra URL segment for the smaller image to find the location of the original
				loc = jQuery(this).attr("src").replace(/styles\/[^\/]*\/public\//,'');
				jQuery(this).wrap('<a href="'+loc+'">');
				el = el.parent();
			}
		}else{
			el = el.parent();
		}
		el.lightbox({opacity:0.5});
	});
});

// Define our custom lightbox
(function($){
	$.fn.lightbox = function(opts){

		// A function to remove the lightbox
		function removeLightbox(){
			$('#lightbox_overlay').remove(); 
			$('#lightbox').remove();
		}
		function isImage(img){
			var i = img.toLowerCase();
			// Only process if it is a known image (could be a link to an arbitrary thing)
			if(i.indexOf('.jpeg') > 0 || i.indexOf('.jpg') > 0 || i.indexOf('.gif') > 0 || i.indexOf('.png') > 0) return true;
			return false;
		}
		function createLightbox(img){
			var w = $(document).width();
			var h = $(document).height();
			var vh = $(window).height();
			// Set the initial size of the lightbox box
			var init_w = (opts.initialWidth ? opts.initialWidth:150);
			var init_h = (opts.initialHeight ? opts.initialHeight:100);
			// How far are we scrolled down the page
			var scroll_top = $(document).scrollTop();
			var f = 0.98;

			// Make the semi-transparent background
			if($('#lightbox_overlay').length==0) $('body').append('<div id="lightbox_overlay" style="z-index:9999;background-color:black;opacity:'+(opts.opacity ? opts.opacity : 0.5)+';-moz-opacity:'+(opts.opacity ? opts.opacity : 0.5)+';filter:alpha(opacity='+(opts.opacity ? opts.opacity*10 : 50)+');position:absolute;top:0px;left:0px;bottom:0px;right:0px;width:'+w+'px;height:'+h+'px;"></div>');
			// If the background is clicked we hide the lightbox
			$('#lightbox_overlay').bind('click',function(){ removeLightbox(); });
			// Make the main part of the lightbox with initial loading message
			if($('#lightbox').length==0) $('body').append('<div id="lightbox" style="z-index:10000;background-color:white;border-radius:8px;position:absolute;top:'+(scroll_top+(vh-init_h)/2)+'px;left:'+((w-init_w)/2)+'px;width:'+init_w+'px;height:'+init_h+'px;"><div id="lightbox_inner" style="margin:16px;max-width:100%;max-height:100%;"><div style="margin-top:'+Math.round((init_h-16)/2)+'px;text-align:center;"><div class="lightbox_loading">Loading...</div></div></div></div>');
			// Load the image off screen
			i = new Image();
			// Once the image is loaded we resize the lightbox
			$(i).bind('load',function(e){
				$(this).removeAttr("width")
				iw = this.width;
				ih = this.height;
				// The box has padding of 32px
				lb_w = iw+32;
				lb_h = ih+32;
				// If the image is larger than the viewport we need to scale it down
				if(lb_h > f*vh){
					lb_h = Math.round(f*vh);
					lb_w = Math.round(lb_h*(iw+32)/(ih+32));
				}
				if(lb_w > f*w){
					lb_w = f*w;
					lb_h = Math.round(lb_w*(ih+32)/(iw+32));
				}
				// Clear the contents and add the loaded image
				$('#lightbox_inner').html('');
				$(this).css({'max-width':'100%','max-height':'100%'});
				$('#lightbox_inner').append(this);
				// Animate the lightbox size/position
				$('#lightbox').css({width:init_w+'px',height:Math.round(init_w*(ih+32)/(iw+32))+'px'}).animate({width:lb_w+'px',height:lb_h+'px',top:(scroll_top+(vh-lb_h)/2)+'px',left:((w-lb_w)/2)+'px' },300).bind('click',function(){ removeLightbox(); });
			}).bind("error",function(e){
				removeLightbox();
				if(typeof e.originalEvent.target.src=="string") window.location.href = e.originalEvent.target.src;
			}).attr({'src':img});
		}
		// Bind a click event to the link that we will turn into a lightbox
		$(this).unbind('click');
		$(this).bind('click',{el:this},function(e){

			// Get the image location
			var img = "";
			if($(this).attr('href')) img = $(this).attr('href');
			else if($(this).attr('src')) img = $(this).attr('src');
			else if($(this).find('img')) img = $(this).find('img').attr('src');

			// Only process if it is a known image (could be a link to an arbitrary thing)
			if(isImage(img)){
				e.preventDefault();
				createLightbox(img);
			}
		});
	};
})(jQuery);