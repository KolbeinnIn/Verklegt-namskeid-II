var navListItems = $('div.setup-panel div p:first-child'),
        allWells = $('.setup-content'),
        allNextBtn = $('.nextBtn'),
        allPrevBtn = $('.prevBtn');

allWells.hide(); //because the payment process is a single application with 4 steps, I hide all the steps
$("#step-1").show() //and only show the first step

//this code is sort of complicated, basically it finds the step that you are currently on using the background of the
//progress bar at the top
//The navigation buttons at the bottom "Til baka" and "Áfram"


allPrevBtn.click(function(){
    let next = get_next_step()
    let uppi_takki_c = navListItems[next-1]
    let uppi_takki_prev = navListItems[next-2]
    $(uppi_takki_c).removeClass('grey-background').addClass('yellow-background');
    $(uppi_takki_prev).addClass('grey-background').removeClass('yellow-background').removeAttr('disabled');
    allWells.hide();
    $(allWells[next-2]).show()
});

let empty = document.getElementById("empty-cart")
if (!empty){
    allNextBtn.click(next_step);
}

function get_phone(){
    return document.getElementById("id_phone_nr")
}


function next_step(){
    let empty = document.getElementById("empty-cart")
    if (empty){
        return false
    }

    let next = get_next_step()
    let $item = $(this);


    var curStep = $item.closest(".setup-content"),
        curInputs = curStep.find("input[type='text'],select"),
        isValid = true;
    let step = curStep[0].getAttribute("id")
    let phone_input = $(get_phone())[0].value
    if ((step === "step-2") && (phone_input.length < 7)){
        create_person_error()
        return false;
    }



    for(let i=0; i< curInputs.length; i++){
        if (!curInputs[i].validity.valid){
            isValid = false;
            $(curInputs[i]).closest(".form-group").addClass("has-error");
        }
    }
    if (isValid){
        let uppi_takki_c = navListItems[next-1]
        let uppi_takki_n = navListItems[next]
        $(uppi_takki_c).removeClass('grey-background').addClass('yellow-background');
        $(uppi_takki_n).addClass('grey-background').removeClass('yellow-background').removeAttr('disabled');
        allWells.hide();
        $(allWells[next]).show()
    }
}

function get_next_step(){
    let item = $('.setup-panel .grey-background')
    let step = item[0].attributes.getNamedItem('custom').value
    return parseInt(step[step.length-1])
}