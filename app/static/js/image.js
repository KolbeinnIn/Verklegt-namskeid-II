let img_counter = 0
function load_img(element){
	let id = element.id
	let img = document.getElementById('img_'+id)
	if (img === null){
		img = document.createElement('img');
		img.setAttribute('id','img_'+id);
		img.setAttribute('src', element.value);
		img.setAttribute('class', 'col-2 staff_product_img mt-2 align-self-center');
		$( img ).insertAfter( $( element ) );
	}
	else{
		img.setAttribute('src', element.value);
	}

}

function delete_input(element){
	let id = element.id.split('_')[1];
	let input = document.getElementById(id);
	let img = document.getElementById('img_'+id);
	element.remove();
	input.remove();
	if (img !== null){
			img.remove();
			console.log(img.id)
		}
	}

function create_img_input(value = ''){
	let element = document.getElementById('image_input');
	var input = document.createElement('input');
	input.setAttribute('id',img_counter);
	input.setAttribute('type','text');
	input.setAttribute('name','image');
	input.setAttribute('class','col-9 form-control mt-2 align-self-center');
	input.setAttribute('oninput','load_img(this)');
	input.value = value;
	let button = document.createElement('button');
	button.innerHTML = 'x';
	button.setAttribute('id','btn_'+img_counter)
	button.setAttribute('class', 'col-0 btn btn-danger align-self-center m-2')
	button.setAttribute('type', 'button')
	button.setAttribute('onclick','delete_input(this)')
	element.appendChild(input);
	element.appendChild(button);
	img_counter +=1;
}

function initialize_images(){
	let container = document.getElementById('image_input');
	let children = [...container.children];
	let input;
	for (let i = 0; i < children.length; i++){
		create_img_input(children[i].src);
		children[i].remove();
	}
	for (let i = 0; i < children.length; i++){
		input = document.getElementById(i);
		load_img(input);
	}
}
initialize_images();