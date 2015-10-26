function timeSpan(span) {
	 end = new Date();

	 start = new Date();
    if (span === 'day') {
		  start.setDate(start.getDate() - 1);
	 } else if (span === 'week') {
		  start.setDate(start.getDate() - 7);
	 } else if (span === 'month') {
		  start.setMonth(start.getMonth() - 1);
	 }

	 console.log(start.toString());

	 $('#start').val((start.getMonth() + 1) + '/' + start.getDate() + '/' + start.getFullYear());
	 $('#end').val((end.getMonth() + 1) + '/' + end.getDate() + '/' + end.getFullYear());
}

function toggleShowClosed() {
 if ($(".closed").css("display") == "none") {
	 $(".closed").css("display", "inline");
 } else {
	 $(".closed").css("display", "none");
 }
}

$(document).ready(function() {
    $('#day').click(function() {
	     timeSpan('day');
    });
    $('#week').click(function() {
	     timeSpan('week');
    });
    $('#month').click(function() {
	     timeSpan('month');
    });

	 $("#toggleShowClosedButton").click(function() {
	     toggleShowClosed();
    });
});
