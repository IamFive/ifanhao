var A = A ? A : {};

A.search = function() {
	var element = $("#f_search input[name=page]");
	var page = (element.length == 1) ? element.val() : '';
	$("#f_search").attr("action", '/a/' + page);
	return true;
};

A.loadMagnet = function(code) {
	$.get('/a/' + code + '/magnet', function(html){
		$('#magnet-content').html(html);
	});
};

A.copy = function(text) {
  window.prompt ("拷贝磁力链(请按下CTRL+C)", text);
};