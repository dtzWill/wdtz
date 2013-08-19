//Run this when the page loads
window.onload = function(){

	//Convert my special tags of skill into actual proper progress bars
	//Just a nice little trick to make writing pages better
	var progressBars = $('.skill');

	for(var i = 0; i < progressBars.length; i++){
		var classes = $(progressBars[i]).attr('class');
		console.log(i + ". Progress " + classes);

		classes = classes.split(" ");

		$(progressBars[i]).append('<div class="progress progress-striped"><div class="bar" style="width: ' +  classes[1]+'%;"></div></div>');

	}
}