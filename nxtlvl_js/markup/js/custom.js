(function() {
 	$('.aside-nav-toggle').on('click', function(event) {
		$(this).parents('#aside-nav').toggleClass('open-nav');
		event.preventDefault();
	});

	$('.btn-toggle-edit').on('click', function(event) {
		$(this).parents('.tasks-table').toggleClass('active-edit');
		event.preventDefault();
	});

	$('.open-action').on('click', function(event) {
		$(this).parents('.priority-list').toggleClass('active-add');
		event.preventDefault();
	});

	$('.toggle-profile-btn').on('click', function(event) {
		$(this).parents('.profile-section').toggleClass('active-profile');
		event.preventDefault();
	});

	$('.open-panel-btn').on('click', function(event) {
		$(this).parents('.control-panel').toggleClass('active-control');
		event.preventDefault();
	});

	$('.slide-opener').on('click', function(event) {
		var opener = $(this);
		var parent = opener.parents('.open-close');
		var slide = parent.find('.slide');
		parent.toggleClass('opened');
		if (parent.hasClass('opened')) {
			slide.slideDown();
		} else {
			slide.slideUp();
		}
		event.preventDefault();
	});

})();
