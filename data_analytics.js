function loadInfo(number){
	var img = document.getElementById("graph");
	var img2 = document.getElementById("graph2");
	if (number == 8 || number == 9)
	{
		console.log("inside the if statement");
		img.src= "subjectivity_chart_question_" + number + ".png";
		img2.src = "polarity_chart_question_" + number + ".png";
		document.body.appendChild(img);
		document.body.appendChild(img2);
		return;
	}
	img2.src = "";
	img.src="histogram_question_" + number + ".png";
	document.body.appendChild(img);
	var text = document.getElementById("data");
	text.innerHTML = "the mode is"
}
var createClickHandler = function(arg) {
  return function() { loadInfo(arg); };
}


function create_entry(){
	console.log("create_entry function is called")
	var i;
	for (i = 0; i < 9; i++) {
		var drop_down_entry = document.createElement("a");
		drop_down_entry.onclick = createClickHandler(i+1)
		drop_down_entry.innerHTML = "Question " + (i+1)
		document.getElementById("ddm").appendChild(drop_down_entry);
	}

}