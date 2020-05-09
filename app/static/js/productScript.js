$(document).ready(function(){

var quantity=0;
   $('.quantity-right-plus').click(function(e){
        // Stop acting like a button
        e.preventDefault();
        // Get the field name
        var quantity = parseInt($('#quantity').val());

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
        // Get the field name
        var quantity = parseInt($('#quantity').val());

        // If is not undefined

            // Increment
            if(quantity>0){
            $('#quantity').val(quantity - 1);
            }
    });

});