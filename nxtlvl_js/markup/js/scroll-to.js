jQuery(function(){
	initPageScroll();
});

// init page scroll
function initPageScroll(){
	jQuery('body').pageScroll({
		links: '.btn-scroll-to',
		animSpeed: 500,
	});
}

/*
 * jQuery Page Scroll Plagin
 */
;(function($) {
	function PageScroll(options) {
		this.options = $.extend({
			activeClass: 'active',
			animSpeed: 1000,
			header: '#header',
			links: 'a'
		}, options);
		this.init();
	}
	PageScroll.prototype = {
		init: function() {
			this.findElements();
			this.attachEvents();
		},
		findElements: function() {
			this.win = $(window);
			this.header = $(this.options.header);
			this.obj = $(this.options.holder);
			this.links = $(this.options.links);
		},
		attachEvents: function() {
			var self = this;
			// links events
			this.links.each(function() {
				var link = $(this);
				var target = $(link.attr('href'));
				if(!target || !target.length) return;
				link.bind('click', function(e){
					e.preventDefault();
					self.scrollTo(target);
				});
			});
			// window events
			this.win.bind('scroll resize orientationchange load', function(){
				self.checkScroll();
			});
		},
		scrollTo: function(value) {
			var skip = 0;
			if(this.header.css('position') === 'fixed') skip = this.header.outerHeight();
			if(typeof value === 'number') {
				$('html, body').stop().animate({scrollTop: value - skip}, {duration: this.options.animSpeed});
			}
			else if(typeof value === 'object') {
				$('html, body').stop().animate({scrollTop: value.offset().top - skip}, {duration: this.options.animSpeed});
			}
		},
		checkScroll: function(){
			var self = this;
			var skip = 0;
			if(this.header.css('position') === 'fixed') skip = this.header.outerHeight();
			this.links.each(function() {
				var link = $(this);
				var target = $(link.attr('href'));
				if(!target || !target.length) return;
				if(self.win.scrollTop() + skip >= target.offset().top && self.win.scrollTop() + skip < target.offset().top + target.outerHeight()){
					link.addClass(self.options.activeClass);
				} else {
					link.removeClass(self.options.activeClass);
				}
			});
		}
	}
	$.fn.pageScroll = function(options) {
		return this.each(function() {
			$(this).data('PageScroll', new PageScroll($.extend(options, {holder: this})));
		})
	}
}(jQuery));