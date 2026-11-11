(function ($) {
    "use strict";
    
    // Dropdown on mouse hover
    $(document).ready(function () {
        function toggleNavbarMethod() {
            if ($(window).width() > 992) {
                $('.navbar .dropdown').on('mouseover', function () {
                    $('.dropdown-toggle', this).trigger('click');
                }).on('mouseout', function () {
                    $('.dropdown-toggle', this).trigger('click').blur();
                });
            } else {
                $('.navbar .dropdown').off('mouseover').off('mouseout');
            }
        }
        toggleNavbarMethod();
        $(window).resize(toggleNavbarMethod);
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Vendor carousel
    $('.vendor-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:2
            },
            576:{
                items:3
            },
            768:{
                items:4
            },
            992:{
                items:5
            },
            1200:{
                items:6
            }
        }
    });


    // Related carousel
    $('.related-carousel').owlCarousel({
        loop: true,
        margin: 29,
        nav: false,
        autoplay: true,
        smartSpeed: 1000,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:2
            },
            768:{
                items:3
            },
            992:{
                items:4
            }
        }
    });


    function paintStars($wrap, value) {
        $wrap.find('i[data-value]').each(function () {
            var n = parseInt($(this).attr('data-value'), 10);
            var filled = n <= value;
            $(this)
                .toggleClass('fas', filled)
                .toggleClass('far', !filled)
                .attr('aria-checked', n === value ? 'true' : 'false');
        });
    }

    $('.star-rating').each(function () {
        paintStars($(this), parseInt($(this).attr('data-rating') || '0', 10));
    });

    $(document).on('mouseenter', '.star-rating i[data-value]', function () {
        paintStars($(this).closest('.star-rating'), parseInt($(this).attr('data-value'), 10));
    });

    $(document).on('mouseleave', '.star-rating', function () {
        paintStars($(this), parseInt($(this).attr('data-rating') || '0', 10));
    });

    $(document).on('click', '.star-rating i[data-value]', function () {
        var value = parseInt($(this).attr('data-value'), 10);
        var $wrap = $(this).closest('.star-rating');
        $wrap.attr('data-rating', value);
        paintStars($wrap, value);
        var $form = $wrap.closest('form');
        var $input = $form.find('input[name="rating"]');
        if (!$input.length) {
            $input = $('#ratingInput');
        }
        $input.val(value);
    });


    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });
    
})(jQuery);

