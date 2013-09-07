var Actors = Actors ? Actors : {};

Actors.search = function() {
	var element = $("#f_search input[name=page]");
	var page = (element.length == 1) ? element.val() : '';
	$("#f_search").attr("action", '/b/' + page);
	return true;
};

Actors.getvideos = function(name) {
	window.location.href = '/a/?k=' + name;
}

$(document).ready(function($) {
	$('a[itemprop=collapse]').on('click', function(e) {
		var $this = $(this);
		var group = $this.attr('group')
		
		// trigger a css toggle
		$('a[itemprop=collapse][group="' + group +'"]').not($this).parents('div.thumbnail').removeClass('thumbnail-info');
		$this.parents('div.thumbnail').addClass('thumbnail-info');
		
		var target  = $this.attr('data-target')
		|| e.preventDefault()
		|| (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') //strip for ie7
		var $target = $(target)
		$('[itemprop=collapse-content][group="' + group +'"]').removeClass('in').addClass('collapse');
	    $target.addClass('in');
	})
});