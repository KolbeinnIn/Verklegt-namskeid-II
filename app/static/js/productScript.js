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
        // If is not undefined

        // Increment
        if(quantity>0){
        $('#quantity').val(quantity - 1);
        }
    });

    $('#addCart').click(function(e){
        let quantity = $('#quantity').val();
        let custom = $(this).attr("custom-link") + "&quantity=" + quantity
        console.log(custom)
        $('#addCart').attr("href", custom);
    });
});