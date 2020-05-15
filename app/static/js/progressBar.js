var navListItems = $('div.setup-panel div p:first-child'),
        allWells = $('.setup-content'),
        allNextBtn = $('.nextBtn'),
        allPrevBtn = $('.prevBtn');

allWells.hide();
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
$("#step-1").show()


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