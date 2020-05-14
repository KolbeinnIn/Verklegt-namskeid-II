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


$('.quantity-right-plus').click(function(e){
    e.preventDefault();

    let qty = get_qty($(this))
    let quantity = parseInt(qty.value);
    let table = $($(this).closest("table")[0])
    let cart = table.attr("cart");
    let url = table.attr("qty-url")
    let cart_item_id = $($(this).closest("tr")[0]).attr("cart-item");

    if(quantity<1000){
        qty.value = quantity + 1;
        update_qty(cart, cart_item_id, qty.value, url)
    }
    else{
        qty.value = 1000;
    }

});

$('.quantity-left-minus').click(function(e){

});

function get_qty(item){
    return item.parent().parent().children('input[id^="quantity-"]')[0]
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
        },
        success: function(obj){
            console.log("ayy lmao", obj)
        }
    })
}


function recieve_updated_cart(){
    $.ajax("/recieve-updated-cart", {
        type: 'GET',
        success: create_review_table
    })
}

function create_review_table(products){
    let table = $("#review-table")
    let total = 0
    for (let i of products){
        let tr = $(document.createElement("tr"))
        tr.addClass("col-12 align-items-center")

        let td_img = $(document.createElement("td"))
        td_img.addClass("d-none d-sm-table-cell py-1 text-center")
        let img = $(document.createElement("img"))
        img.attr("src", i.image)
        img.addClass("small_image_thumbnail")
        td_img.append(img)
        tr.append(td_img)

        let td_name = $(document.createElement("td"))
        td_name.text(i.name)
        tr.append(td_name)


        let td_qty = $(document.createElement("td"))
        let p_qty = $(document.createElement("p"))
        p_qty.addClass("text-center")
        p_qty.text(i.quantity)
        td_qty.append(p_qty)
        tr.append(td_qty)

        let td_price = $(document.createElement("td"))
        td_price.addClass("text-center")
        let price = i.quantity * i.price
        total = total+price
        td_price.text(price.toString()+" kr")
        tr.append(td_price)
        table.append(tr)
    }
    let new_tr = $(document.createElement("tr"))
    new_tr.addClass("col-12")

    let filler_td = $(document.createElement("td"))
    filler_td.addClass("d-none d-sm-table-cell")

    let samtals_td = $(document.createElement("td"))
    samtals_td.addClass("text-right pr-0")
    let stronk = $(document.createElement("strong"))
    stronk.text("Samtals:")
    samtals_td.append(stronk)

    let total_td = $(document.createElement("td"))
    total_td.addClass("text-center pr-0")
    let total_stronk = $(document.createElement("strong"))
    total_stronk.addClass("text-right")
    total_stronk.text(total.toString()+ " kr")
    total_td.append(total_stronk)


    new_tr.append(filler_td)
    new_tr.append(document.createElement("td"))
    new_tr.append(samtals_td)
    new_tr.append(total_td)
    table.append(new_tr)
}

nextBtn = $('.nextBtn')[0].addEventListener("click", recieve_updated_cart)


$($('input[id^="quantity-"]')[0]).change(function(e){
    e.preventDefault()
    let qty = get_qty($(this))
    console.log("lala", qty)
    let quantity = parseInt(qty.value);
    let table = $($(this).closest("table")[0])
    let cart = table.attr("cart");
    let url = table.attr("qty-url")
    let cart_item_id = $($(this).closest("tr")[0]).attr("cart-item");
    if(quantity>1){
            qty.value = quantity;
            update_qty(cart, cart_item_id, qty.value, url)
    }
});
