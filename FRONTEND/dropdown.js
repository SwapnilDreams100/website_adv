var arr = ['q1','q2','q3','q4','q5','q6','q7','q8'];
function findDay()
{
	$('#prompt_q').empty()
	var eID = document.getElementById("prompts");
	var dayVal = eID.options[eID.selectedIndex].value;
	var daytxt = eID.options[eID.selectedIndex].text;
	data_pass['prompt'] = dayVal
	$('#prompt_q').append(arr[dayVal-1]);
	$('#prompt_q').show()
}

function findFeed()
{
	$('#feed_q').empty()
	var eID = document.getElementById("feedback_scores");
	// var dayVal = eID.options[eID.selectedIndex].value;
	var daytxt = eID.options[eID.selectedIndex].text;
	data_pass['feedback_score'] = daytxt
	$('#feed_q').append(daytxt);
	$('#feed_q').show()
	
}