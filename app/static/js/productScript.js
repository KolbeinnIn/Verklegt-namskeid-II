$(document).ready(function(){


    $('.quantity-right-plus').click(function(e){
        // Stop acting like a button
        e.preventDefault();
        let quantity = parseInt($('#quantity').val());

        // If is not undefined

            // Increment
            if(quantity<1000){
                $('#quantity').val(quantity + 1);
            }
            else{
                $('#quantity').val(1000);
            }
    });

    $('.quantity-left-minus').click(function(e){
        // Stop acting like a button
        e.preventDefault();
        let quantity = parseInt($('#quantity').val());

        if(quantity>1){
        $('#quantity').val(quantity - 1);
        }
    });
     $('')

    $('#addCart').click(function(e){ //makes the add to cart button add the right product to the cart with right quantity
        let quantity = $('#quantity').val();
        let custom = $(this).attr("custom-link") + "&quantity=" + quantity
        $('#addCart').attr("href", custom);
    });
});