$('#id_card_number').on('keypress change', function () {
  $(this).val(function (index, value) {
    return value.replace(/\W/gi, '').replace(/(.{4})/g, '$1 ');
  });
});

$('#id_expiration_date').on('keypress change', function () {
  $(this).val(function (index, value) {
    return value.replace(/\W/gi, '').replace(/(.{2})/g, '$1 ');
  });
});

review = document.getElementById("review_btn")
review.addEventListener("click", function(){
    //the review-btn is in the payment details part of the site,
    //this function adds the personal and payment information to the review site
    let number = document.getElementById("id_card_number").value
    let name = document.getElementById("id_cardholder_name").value
    let exp = document.getElementById("id_expiration_date").value
    let cvc = document.getElementById("id_cvc").value
    number = number.replace(/ /g, '');

    let og_exp = exp
    let exp_arr = new Array()
    exp_arr.push(og_exp.slice(0,2))
    exp_arr.push(og_exp.slice(3,5))

    let regex = new RegExp("^[0-9]{16}$");
    let correct = false
    if (!regex.test(number) || (name === "" || og_exp === "" || cvc.toString().length !== 3 || !isInt(cvc))){
        //if the card number is "valid" (16 integers) or any of the other fields are empty then display an error
        $("#payment_warning").remove()
        create_error("payment_form_parent")
    }
    else{
        correct = true
    }
    if (correct){
        if (((parseInt(exp_arr[0]) < 0) || (parseInt(exp_arr[0]) > 31)) || ((parseInt(exp_arr[1]) < 0) || (parseInt(exp_arr[1]) > 12))){
            $("#payment_warning").remove()
            create_error("payment_form_parent")
        }
        else{ //if everything is A-okay then I write all of the information to the review page and then display it
            let exp_1 = parseInt(exp_arr[0])
            let exp_2 = parseInt(exp_arr[1])
            get_personal_info()
            get_payment_info(number, exp_1, exp_2)
            next_step()
            $("#payment_warning").remove()
        }
    }
})

function isInt(num){
    return !isNaN(num)
}

function create_error(id){
    let elem = $("#"+id)
    let new_warning = document.createElement("div")
    new_warning.setAttribute("id", "payment_warning")
    new_warning.setAttribute("class", "alert alert-danger")
    new_warning.textContent = "Þessar kortaupplýsingar eru ekki gildar!"
    elem.prepend(new_warning);
}

function create_person_error(){
    let elem = $("#personal_info_form")
    let new_warning = document.createElement("div")
    new_warning.setAttribute("id", "payment_warning")
    new_warning.setAttribute("class", "alert alert-danger")
    new_warning.textContent = "Þetta símanúmer er ekki gilt!"
    elem.prepend(new_warning);
}

function create_elem(name, inner){ //just to create the elements that display the payment and personal information
    let new_elem = document.createElement("p")
    let inner_elem = document.createElement("b")
    new_elem.textContent = name+": "
    inner_elem.textContent = inner
    new_elem.appendChild(inner_elem)
    return new_elem
}

function get_personal_info(){ //writes the personal info on the review page
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
    let info_obj = { //this object gets sent through an ajax request
        "first_name":fn,
        "last_name": ln,
        "phone":phone,
        "city": city,
        "address": address,
        "zip":zip,
        "country": country_str
    }
    let info_list = [ //this list is used to display the data on the review page
        ["Fornafn",fn],
        ["Eftirnafn",ln],
        ["Sími",phone],
        ["Borg/bær", city],
        ["Heimilisfang",address],
        ["Póstnúmer",zip],
        ["Land",country_str],
    ]
    for (let i of info_list){
        let info_piece = create_elem(i[0], i[1])
        sth.append(info_piece)
    }
    let og_cart = $("#og-cart")[0]
    let cart_id = og_cart.getAttribute("cart")
    let url = og_cart.getAttribute("person-info")
    update_personal_info(cart_id, info_obj, url) //this function sends an ajax request to update the personal information associated with the cart
}


function get_payment_info(card, exp_1, exp_2){ //writes the payment information on the review page as well as shipping
    let sth = $("#payment_info_review")
    sth.children("p").remove()
    let last_digits = card.substr(card.length-4)
    card = "XXXX-XXXX-XXXX-"+last_digits
    let info_list = [
        ["Nafn korthafa",document.getElementById("id_cardholder_name").value],
        ["Kortanúmer",card],
        ["Gildistími",exp_1.toString()+" "+exp_2.toString()],
        ["CVC",document.getElementById("id_cvc").value]
    ]
    for (let i of info_list){
        let info_piece = create_elem(i[0], i[1])
        sth.append(info_piece)
    }
    let afh = document.createElement("h4")
    let afh_u = document.createElement("u")
    afh_u.textContent = "Afhendingarmáti"
    afh.appendChild(afh_u)
    sth.append(afh)
    let shipping = document.createElement("p")
    shipping.textContent = get_shipping_str()
    sth.append(shipping)
}

function update_personal_info(cart_id, info_list, url){
    let csrf = $('[name="csrfmiddlewaretoken"]')[0].value;
    $.ajax(url, {
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf
        },
        data: JSON.stringify({
            "cart_id": cart_id,
            "personal_info": info_list,
            "shipping": get_shipping_str()
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
        }
    })
}
function recieve_updated_cart(){
    $.ajax("/recieve-updated-cart", {
        type: 'GET',
        success: create_review_table
    })
}
function create_review_table(products){ // Create table from the updated product list that I got from the ajax request
    //this function looks very long and complicated but it's really not, just takes a list of products displays them on review page
    let table = $("#review-table")
    $(table).find("tbody").empty()
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

//the first "Áfram" button on the cart page recieves the updated cart through an ajax request and sends the cart to the function above (create_review_table)
$('.nextBtn')[0].addEventListener("click", recieve_updated_cart)

function change_qty(e){
    //this function gathers all the required information about the cart and its items and sends ajax request to update the quantity in the database
    //and of course display the new quantity
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
    update_qty(cart, cart_item_id, qty.value, url)
    update_total(row, qty.value);
}

let qty_input = ($('input[id^="quantity-"]'))

qty_input.keydown(function(e) {
    //this is only here because the payment process uses only a single page,
    //the page has 2 different forms on two different steps (personal info and payment info)
    //so if you press enter on the cart portion you submit the forms that are empty and that causes and error in the console
    //this function prevents that
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if(keycode === 13){
        e.preventDefault()
    }
});

qty_input.change(change_qty); //sends ajax request every time the quantity of any product in the cart is updated

function update_total(row, qty){
    let unit_price = parseInt(row.attr("unit-price"))
    let new_price = unit_price*qty
    let price_str = row.find(".price")[0].textContent
    let price = parseInt(price_str.substring(0, price_str.length-3));
    row.find(".price")[0].textContent = new_price.toString() + " kr"
    let total_str = $("#cart-total")[0]
    let total = parseInt(total_str.textContent.substring(0, total_str.textContent.length-3));
    total_str.textContent = ((total-price)+new_price).toString() + " kr"
}

let remove_buttons = $('.remove_item')
remove_buttons.click(remove_item)

function remove_item(e){ //removes a product from the cart and updates the cart total accordingly
    e.preventDefault()
    let button = $(this)
    let row = button.closest("tr")
    let table = $("#og-cart")[0]
    let url = table.getAttribute("trash-url")
    update_total(row, 0) //update the cart total

    let cart_id = table.getAttribute("cart");
    let cart_item_id = $($(this).closest("tr")[0]).attr("cart-item");

    remove_item_ajax(cart_id, cart_item_id, url) //sends an ajax request to update the database with the product removed from the cart
    $(row).remove() //removes the product visually

    let children = $($(table)[0]).find("tbody tr").length //get number of rows in the table (products + row that displays total price)
    if (children === 1){ //=== 1 because cart total will be the only row in the table aka no products in the cart,
        // then I add an indicator to tell customer that the cart is empty with id = "empty-cart", the id will block the "Áfram" button.
        let table_parent = $(table).parent()
        $(table).remove()
        let empty_cart = document.createElement("h2")
        $(empty_cart).attr("id", "empty-cart").text("Karfan er tóm")
        table_parent.append(empty_cart)
    }
}
function remove_item_ajax(cart_id, cart_item_id, url){ //tells the backend which product was removed
    let csrf = $('[name="csrfmiddlewaretoken"]')[0].value;
    $.ajax(url, {
        type: 'POST',
        headers: {
            'X-CSRFToken': csrf
        },
        data: {
            "cart_id": cart_id,
            "cart_item_id": cart_item_id
        }
    })
}
function get_shipping_str(){
    //this is to create the string necessary to display what type of shipping the user selected
    //this function is also used to send what type of shipping the cart should store in the database
    let shipping = $("#shipping").find("input")
    for (let i of shipping){
        if (i.checked){
            let ship_id = i.value;
            if (ship_id == 1){
                return "Sótt í verslun"
            }
            else{
                return "Heimsending"
            }
        }
    }
}



