function create_elem(name, inner){
    new_elem = document.createElement("p")
    inner_elem = document.createElement("b")
    new_elem.textContent = name+": "
    inner_elem.textContent = inner
    new_elem.appendChild(inner_elem)
    return new_elem
}

function get_personal_info(){
    sth = document.getElementById("personal_info_review")
    country = document.getElementById("id_country")
    info_list = [
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
        sth.appendChild(info_piece)
    }
}

function get_payment_info(){
    sth = document.getElementById("personal_info_review")
    country = document.getElementById("id_country")
    info_list = [
        ["First name",document.getElementById("id_first_name").value],
        ["Last name",document.getElementById("id_last_name").value],
        ["Phone",document.getElementById("id_phone_nr").value],
        ["City",document.getElementById("id_city").value]
    ]
    for (let i of info_list){
        info_piece = create_elem(i[0], i[1])
        sth.appendChild(info_piece)
    }
}