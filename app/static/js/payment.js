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
    number = number.replace(/ /g, '');

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
        next_step()
        $("#payment_warning").remove()

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



let first_btn = $('a[ref="#step-1"]')[0]
first_btn.addEventListener("click", get_new_cart)


$('.quantity-right-plus').click(function(e){
    e.preventDefault();

    let qty = get_qty($(this))
    let quantity = parseInt(qty.value);
    let cart = $($(this).closest("table")[0]).attr("cart");
    let cart_item_id = $($(this).closest("tr")[0]).attr("cart-item");

    if(quantity<1000){
        qty.value = quantity + 1;
        update_qty(cart, cart_item_id, qty.value, "INSERT URL")
    }

    else{
        qty.value = 1000;
    }

});

$('.quantity-left-minus').click(function(e){
    e.preventDefault();
    let qty = get_qty($(this))
    let quantity = parseInt(qty.value);
    if(quantity>1){
            qty.value = quantity - 1;
            update_qty(cart, cart_item_id, qty.value, "INSERT URL")
    }
});

function get_qty(item){
    return item.parent().parent().children('input[id^="quantity-"]')[0]
}


function get_new_cart(){
    let table = $("#og-cart");
    let cart_id = table.attr("cart")
    let url = table.attr('change-quantity')
    let products = $(table.children("tbody")[0]).children("tr");
    let a = $(table).find(".input-group");

    for (let i=0; i<products.length-1; i++){
        let quantity = parseInt($(a[i]).find('input[name="quantity"]').val())
        let unit_price = parseInt($(products[i]).attr("unit-price"))
        let prod_id = parseInt($(products[i]).attr("prod-id"))
        let cart_item = parseInt($(products[i]).attr("cart-item"))
        console.log(quantity, unit_price, prod_id, cart_item)
    }
}

function update_qty(cart_id, cart_item_id, quantity, url){
    let csrf = $('[name="csrfmiddlewaretoken"]')[0].value;
    $.ajax(url, {
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf
        },
        data: {
            "cart_id": cart_id,
            "cart_item_id": cart_item_id,
            "quantity": quantity
        }
    })
}

$($('input[id^="quantity-"]')[0]).change(function(e){
   console.log("ayy lmao")
});