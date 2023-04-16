(function ($) {
    "use strict";
    
    // // Dropdown on mouse hover
    // $(document).ready(function () {
    //     function toggleNavbarMethod() {
    //         if ($(window).width() > 992) {
    //             $('.navbar .dropdown').on('mouseover', function () {
    //                 $('.dropdown-toggle', this).trigger('click');
    //             }).on('mouseout', function () {
    //                 $('.dropdown-toggle', this).trigger('click').blur();
    //             });
    //         } else {
    //             $('.navbar .dropdown').off('mouseover').off('mouseout');
    //         }
    //     }
    //     toggleNavbarMethod();
    //     $(window).resize(toggleNavbarMethod);
    // });
    
    
    // // Back to top button
    // $(window).scroll(function () {
    //     if ($(this).scrollTop() > 100) {
    //         $('.back-to-top').fadeIn('slow');
    //     } else {
    //         $('.back-to-top').fadeOut('slow');
    //     }
    // });
    // $('.back-to-top').click(function () {
    //     $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
    //     return false;
    // });


    // // Vendor carousel
    // $('.vendor-carousel').owlCarousel({
    //     loop: true,
    //     margin: 29,
    //     nav: false,
    //     autoplay: true,
    //     smartSpeed: 1000,
    //     responsive: {
    //         0:{
    //             items:2
    //         },
    //         576:{
    //             items:3
    //         },
    //         768:{
    //             items:4
    //         },
    //         992:{
    //             items:5
    //         },
    //         1200:{
    //             items:6
    //         }
    //     }
    // });


    // // Related carousel
    // $('.related-carousel').owlCarousel({
    //     loop: true,
    //     margin: 29,
    //     nav: false,
    //     autoplay: true,
    //     smartSpeed: 1000,
    //     responsive: {
    //         0:{
    //             items:1
    //         },
    //         576:{
    //             items:2
    //         },
    //         768:{
    //             items:3
    //         },
    //         992:{
    //             items:4
    //         }
    //     }
    // });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 1) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });
    
})(jQuery);


var updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function() {
    const productId = this.dataset.product;
    const action = this.dataset.action;

    console.log('Product Id: ', productId)
    console.log('Action: ', action)
    // console.log('User: ', user)

    var url = '/update-item/'
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({'productId':productId, 'action':action})
    })
      .then((response) => {
        return response.json()
      })
      .then(data => {
        console.log(data)
        //Update the quantity value on the page
        var quantityElem = document.getElementById(`quantity_${productId}`);
        if (quantityElem) {
          quantityElem.textContent = data.quantity;
        }

        var priceElem = document.getElementById(`price_${productId}`);
        if (priceElem) {
          priceElem.textContent = '$' + data.price;
        }

        var orderpriceElem = document.getElementById(`order-price`);
        if (orderpriceElem) {
          orderpriceElem.textContent = '$' + data.order_price;
        }

        var ordertotalElem = document.getElementById(`total-price`);
        if (ordertotalElem) {
          ordertotalElem.textContent = '$' + data.total_price;
        }

        var countElem = document.getElementById(`order-count`);
        if (countElem) {
          countElem.textContent = data.count;
        }

      })
  })
}

// Delete button
var removeButtons = document.getElementsByClassName('btn-delete');

for (let i = 0; i < removeButtons.length; i++) {
  removeButtons[i].addEventListener('click', function() {
    var row = document.getElementById(this.dataset.product);

    row.remove();
  });
}