$('#id_card_number').on('keypress change', function () {
  $(this).val(function (index, value) {
    return value.replace(/\W/gi, '').replace(/(.{4})/g, '$1 ');
  });
});

review = document.getElementById("review_btn")
review.addEventListener("click", function(){
    let number = document.getElementById("id_card_number").value

    let name = document.getElementById("id_cardholder_name").value
    let exp = document.getElementById("id_expiration_date").value
    let cvc = document.getElementById("id_cvc").value

    console.log(number)
    number = number.replace(/ /g, '');
    console.log(number)
    let regex = new RegExp("^[0-9]{16}$");
    if (!regex.test(number) || (name === "" || exp === "" || cvc === "")){
        $("#payment_warning").remove()
        let new_warning = document.createElement("div")
        new_warning.setAttribute("id", "payment_warning")
        new_warning.setAttribute("class", "alert alert-danger")
        new_warning.textContent = "Þessar kortaupplýsingar eru ekki gildar!"
        $("#payment_form_parent").prepend(new_warning);
    }
    else{
        get_personal_info()
        get_payment_info(number)
        $("#step-3").hide()
        $("#step-4").show()
    }
})


function create_elem(name, inner){
    let new_elem = document.createElement("p")
    let inner_elem = document.createElement("b")
    new_elem.textContent = name+": "
    inner_elem.textContent = inner
    new_elem.appendChild(inner_elem)
    return new_elem
}

function get_personal_info(){

    let sth = $("#personal_info_review")
    sth.children("p").remove()
    let country = document.getElementById("id_country")
    let info_list = [
        ["First name",document.getElementById("id_first_name").value],
        ["Last name",document.getElementById("id_last_name").value],
        ["Phone",document.getElementById("id_phone_nr").value],
        ["City",document.getElementById("id_city").value],
        ["Address",document.getElementById("id_address").value],
        ["Zip code",document.getElementById("id_zip_code").value],
        ["Country",country[country.value].textContent],
    ]
    for (let i of info_list){
        info_piece = create_elem(i[0], i[1])
        sth.append(info_piece)
    }
}

function get_payment_info(card){

    let sth = $("#payment_info_review")
    sth.children("p").remove()
    let last_digits = card.substr(card.length-4)
    card = "XXXX-XXXX-XXXX-"+last_digits
    let info_list = [
        ["Nafn korthafa",document.getElementById("id_cardholder_name").value],
        ["Kortanúmer",card],
        ["Gildistími",document.getElementById("id_expiration_date").value],
        ["CVC",document.getElementById("id_cvc").value]
    ]
    for (let i of info_list){
        let info_piece = create_elem(i[0], i[1])
        sth.append(info_piece)
    }
}