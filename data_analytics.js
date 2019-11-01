function loadInfo(number){
	var img = document.getElementById("graph");
	img.src="histogram_question_" + number + ".png";
	document.body.appendChild(img);
	var text = document.getElementById("data");
	text.innerHTML = "the mode is"
}