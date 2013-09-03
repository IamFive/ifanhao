var A = A ? A : {};

A.search = function() {
	var element = $("#f_search input[name=page]");
	var page = (element.length == 1) ? element.val() : '';
	$("#f_search").attr("action", '/a/' + page);
	return true;
}