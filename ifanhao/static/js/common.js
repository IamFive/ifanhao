(function($) {

	$(document).ready(function($) {
		// toggle tooltip
		$('[data-toggle="tooltip"]').tooltip();
	});

})($);


var Paginate = {};

Paginate.paginate = function(formname, page) {
	var exists = ($("#" + formname + " input[name=page]").length == 1)
	if (!exists) {
		$("<input>").attr({
			type : "hidden",
			name : "page",
			value : page
		}).appendTo($("#" + formname))
	} else {
		$("#" + formname + " input[name=page]").attr("value", page)
	}

	$("#" + formname).submit();
}