var question_info = [];

function loadInfo(number){
	var img = document.getElementById("graph");
	var img2 = document.getElementById("graph2");
	var text = document.getElementById("data");
	for (i = 0 ; i<question_info.length; i++)
	{
		if (question_info[i][1] == number)
		{
			if (question_info[i][0] == "open_ended")
			{
				console.log("inside the if statement");
				img.src= "subjectivity_chart_question_" + number + ".png";
				img2.src = "polarity_chart_question_" + number + ".png";
				document.body.appendChild(img);
				document.body.appendChild(img2);
				text.innerHTML = "Percentage positive response: "+ question_info[i][2]+"%"
								+"<br> <br> Percentage negative response: "+ question_info[i][3]+"%"
								+"<br> <br> Percentage subjective: "+ question_info[i][4]+"%" 
								+"<br> <br> Percentage objective: "+ question_info[i][5]+"%" 
								+ "<br> <br> Percentage netural: "+ question_info[i][6]+"%"; 
				return;
			}
			img2.src = "";
			img.src="histogram_question_" + number + ".png";
			document.body.appendChild(img);
			text.innerHTML ="<br> <br> Mean: "+ question_info[i][3]
							+"<br> <br> Mode: "+ question_info[i][4] 
							+"<br> <br> Median: "+question_info[i][5]
							+"<br> <br> Standard Deviation: "+question_info[i][6];
		}

	}
}
var createClickHandler = function(arg) {
  return function() { loadInfo(arg); };
}


function create_entry(){
	console.log("create_entry function is called")
	var i;
	for (i = 0; i < 20; i++) {
		var drop_down_entry = document.createElement("a");
		drop_down_entry.onclick = createClickHandler(i+1)
		drop_down_entry.innerHTML = "Question " + (i+1)
		document.getElementById("ddm").appendChild(drop_down_entry);
	}

}


$.ajaxPrefilter( 'text', function( options ) {
    options.crossDomain = true;
});

$.ajax({
    type: "GET",
    url: "analytics.csv",
    dataType: "text",
    success: function(data) {
        //alert("worked");
   		parse(data);
    },
    error: function (request, status, error) {

        alert(error);
    }
 });

/*function parse_data(allText){
	var question_number = 1;
	var allTextLines = allText.split(/\r\n|\n/);
	console.log(allTextLines.length);
	var i;
	for (i=0; i<allTextLines.length; i++){
		var entry = allTextLines[i]
		if (entry.length!=0){
			console.log(i);

			var instance = entry.split(',');
			if (instance[0] == "multiple_choice" || instance[0] == "open_ended")
			{
				question_info.push(instance);
			}
		}
	}
	var j;
	for (j=0;j<question_info.length;j++)
	{
		console.log(question_info[j]);
	}
}*/

function parse(allText){
	var question_number=1;
	var allTextLines = Papa.parse(allText).data;
	var i;
	for (i=0; i<allTextLines.length; i++){
		var entry = allTextLines[i]
		if (entry.length!=1){
			console.log(i);
			console.log("this is the entry:",entry,"the length of entry is:", entry.length);
			if (entry[0] == "multiple_choice" || entry[0] == "open_ended")
			{
				question_info.push(entry);
			}
		}
	}
	var j;
	for (j=0;j<question_info.length;j++)
	{
		console.log(question_info[j]);
	}
}