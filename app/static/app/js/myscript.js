$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data:{
            prod_id : id
        }, //aita ai url a data sent hobe
        success: function(data) {
            // console.log(data)
            // parseFloat(a).toFixed(1); to make it float number use this
            eml.innerText = data.quantity
            var amount = data.amount
            var totalamount = data.totalamount
            document.getElementById("amount").innerText = parseFloat(amount).toFixed(1);
            document.getElementById("totalamount").innerText = parseFloat(totalamount).toFixed(1);
        } // aita django theke data niye html a show korbe
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data:{
            prod_id : id
        }, 
        success: function(data) {
            eml.innerText = data.quantity
            var amount = data.amount
            var totalamount = data.totalamount
            document.getElementById("amount").innerText = parseFloat(amount).toFixed(1);
            document.getElementById("totalamount").innerText = parseFloat(totalamount).toFixed(1);
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.parentNode.parentNode.parentNode
    // console.log(id)
    $.ajax({
        type: "GET",
        url: "/removecart",
        data:{
            prod_id : id
        },
        success: function(data) {
            var amount = data.amount
            var totalamount = data.totalamount
            if(amount==0){
                var shipping = 0
                totalamount = 0 
            }else{
                var shipping = 70 
            }
            document.getElementById("amount").innerText = parseFloat(amount).toFixed(1);
            document.getElementById("totalamount").innerText = parseFloat(totalamount).toFixed(1);
            document.getElementById("shipping").innerText = parseFloat(shipping).toFixed(1);
            eml.remove()
            document.getElementById("ct-n").innerText = data.c_num;
        }
    })
})


function cartvalue(){
    $.ajax({
        type: "GET",
        url: "/cart_status",
        success: function(data) {
            var c_num = data.c_num
            document.getElementById("ct-n").innerText = c_num;
        }
    })
}
