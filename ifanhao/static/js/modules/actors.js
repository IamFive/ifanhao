var Actors = Actors ? Actors : {};

Actors.search = function() {
	var element = $("#f_search input[name=page]");
	var page = (element.length == 1) ? element.val() : '';
	$("#f_search").attr("action", '/b/' + page);
	return true;
}