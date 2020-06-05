var owl = $('.owl-carousel');
owl.owlCarousel({
    margin:10,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:3
        },            
        960:{
            items:4
        }
    }
});
