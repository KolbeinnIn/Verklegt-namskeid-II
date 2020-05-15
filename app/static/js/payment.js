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
    let fn = document.getElementById("id_first_name").value
    let ln = document.getElementById("id_last_name").value
    let phone = document.getElementById("id_phone_nr").value
    let city = document.getElementById("id_city").value
    let address = document.getElementById("id_address").value
    let zip = document.getElementById("id_zip_code").value
    let country_str = country[country.value].textContent

    let info_obj = {
        "first_name":fn,
        "last_name": ln,
        "phone":phone,
        "city": city,
        "address": address,
        "zip":zip,
        "country": country_str
    }

    let info_list = [
        ["First name",fn],
        ["Last name",ln],
        ["Phone",phone],
        ["City", city],
        ["Address",address],
        ["Zip code",zip],
        ["Country",country_str],
    ]
    for (let i of info_list){
        let info_piece = create_elem(i[0], i[1])
        sth.append(info_piece)
    }

    let og_cart = $("#og-cart")[0]
    let cart_id = og_cart.getAttribute("cart")
    let url = og_cart.getAttribute("person-info")
    console.log(info_obj)
    update_personal_info(cart_id, info_obj, url)
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

function update_personal_info(cart_id, info_list, url){
    let csrf = $('[name="csrfmiddlewaretoken"]')[0].value;
    $.ajax(url, {
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf
        },
        data: JSON.stringify({
            "cart_id": cart_id,
            "personal_info": info_list
        }),
    })
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
        success: function(){
            console.log("Ayy lmao")
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

$('.nextBtn')[0].addEventListener("click", recieve_updated_cart)


function change_qty(e){
    let qty = $(this)[0]
    let row = $(qty).closest("tr")
    let quantity = parseInt(qty.value);
    let table = $($(this).closest("table")[0])
    let cart = table.attr("cart");
    let url = table.attr("qty-url")
    let cart_item_id = $($(this).closest("tr")[0]).attr("cart-item");
    if(quantity>1){
            qty.value = quantity;
    }
    if(quantity > 1000){
            qty.value = 1000;
    }
    if (quantity < 1){
            qty.value = 1;
    }
    console.log("for inn")
    update_qty(cart, cart_item_id, qty.value, url)
    update_total(row, qty.value);
}

let qty_input = ($('input[id^="quantity-"]'))

qty_input.keydown(function(e) {
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if(keycode === 13){
        e.preventDefault()
    }
});

qty_input.change(change_qty);


function update_total(row, qty){
    let unit_price = parseInt(row.attr("unit-price"))
    let new_price = unit_price*qty
    let price_str = row.find(".price")[0].textContent
    let price = parseInt(price_str.substring(0, price_str.length-3));
    row.find(".price")[0].textContent = new_price.toString() + " kr"
    let total_str = $("#cart-total")[0]
    let total = parseInt(total_str.textContent.substring(0, total_str.textContent.length-3));
    total_str.textContent = ((total-price)+new_price).toString() + " kr"
    console.log(total_str.textContent)
    console.log(total, price, new_price, (total-price)+new_price)
}