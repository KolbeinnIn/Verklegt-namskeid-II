function create_img_input(element){
	var input = document.createElement("input");
	input.setAttribute('type',"text");
	input.setAttribute('class',"image")
	input.setAttribute('class','form-control')
	$( input ).insertAfter( $( element ) );
	}