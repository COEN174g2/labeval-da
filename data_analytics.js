var question_info = [];

function loadInfo(number){
	var img = document.getElementById("graph");
	var img2 = document.getElementById("graph2");
	var text = document.getElementById("data");
	if (question_info[number-1][0] == "open_ended")
	{
		console.log("inside the if statement");
		img.src= "subjectivity_chart_question_" + number + ".png";
		img2.src = "polarity_chart_question_" + number + ".png";
		document.body.appendChild(img);
		document.body.appendChild(img2);
		text.innerHTML = "percentage positive response:"+ question_info[number-1][1] 
						+"\npercentage negative response:"+ question_info[number-1][2] 
						+"\npercentage subjective:"+ question_info[number-1][3] 
						+"\npercentage objective:"+ question_info[number-1][4] 
						+ "\npercentage netural:"+ question_info[number-1][5]; 
		return;
	}
	img2.src = "";
	img.src="histogram_question_" + number + ".png";
	document.body.appendChild(img);
	text.innerHTML = " the most popular choice:" + question_info[number-1][1] 
					+ "\nmean:"+ question_info[number-1][2]
					+"\nmode:"+ question_info[number-1][3] 
					+"\nmedian:"+question_info[number-1][4]
					+"\nstandard_deviation:"+question_info[number-1][5];
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

/*function readTextFile(file)
{
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                console.log(allText);
            }
        }
    }
    rawFile.send(null);
}


readTextFile("analytics.csv")*/

$.ajaxPrefilter( 'text', function( options ) {
    options.crossDomain = true;
});

$.ajax({
    type: "GET",
    url: "analytics.csv",
    dataType: "text",
    success: function(data) {
        //alert("worked");
   		parse_data(data);
    },
    error: function (request, status, error) {

        alert(error);
    }
 });

function parse_data(allText){
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
}