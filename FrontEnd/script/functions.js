jQuery(document).ready(function($) {

    'use strict';
    
    // Banner Slider Function
    $('.ritekhed-banner').slick({
      dots: false,
      infinite: true,
      arrows: false,
      speed: 1000,
      autoplay: true,
      fade: true,
      autoplaySpeed: 2000,
      slidesToShow: 1,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });
    // Fixture Table Slider Function
    $('.ritekhed-fixture-table-slider').slick({
      dots: false,
      infinite: true,
      prevArrow: "<span class='slick-arrow-left'><i class='fa fa-chevron-left'></i></span>",
      nextArrow: "<span class='slick-arrow-right'><i class='fa fa-chevron-right'></i></span>",
      speed: 1000,
      autoplay: true,
      fade: false,
      autoplaySpeed: 2000,
      slidesToShow: 8,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });
    // Testimonial Slider Function
    $('.ritekhed-testimonial-slider').slick({
      dots: false,
      infinite: true,
      prevArrow: "<span class='slick-arrow-left'><i class='fa fa-chevron-left'></i></span>",
      nextArrow: "<span class='slick-arrow-right'><i class='fa fa-chevron-right'></i></span>",
      speed: 1000,
      autoplay: true,
      fade: false,
      autoplaySpeed: 2000,
      slidesToShow: 3,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1,
            infinite: true,
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });
    // Partner Slider Function
    $('.ritekhed-partner-slider').slick({
      dots: false,
      infinite: true,
      prevArrow: "<span class='slick-arrow-left'><i class='fa fa-chevron-left'></i></span>",
      nextArrow: "<span class='slick-arrow-right'><i class='fa fa-chevron-right'></i></span>",
      speed: 1000,
      autoplay: true,
      fade: false,
      autoplaySpeed: 2000,
      slidesToShow: 4,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });

    // Responsive Main Menu Function
    jQuery('#main-menu').smartmenus({
      subMenusSubOffsetX: 1,
      subMenusSubOffsetY: -10
    });

    // Menu Link Function
    jQuery( ".ritekhed-menu-link" ).on("click", function() {
      jQuery( "#main-nav" ).slideToggle( "slow", function() {
      });
    });

    //*** Function CartToggle
    jQuery('a.ritekhed-open-cart').on("click", function(){
          jQuery('.ritekhed-cart-box').slideToggle('slow');
          return false;
      });
      jQuery('html').on("click", function() { jQuery(".ritekhed-cart-box").fadeOut(); });
      
      //*** Function Counter
      jQuery('#word-count1').jQuerySimpleCounter({
        end:15000,
        duration: 5000
      });
      jQuery('#word-count2').jQuerySimpleCounter({
        end:70000,
        duration: 5000
      });
      jQuery('#word-count3').jQuerySimpleCounter({
        end:30000,
        duration: 5000
      });
      jQuery('#word-count4').jQuerySimpleCounter({
        end:50000,
        duration: 5000
      });

    //***************************
    // Countdown Function
    //***************************
    jQuery(function() {
        var austDay = new Date();
        austDay = new Date(austDay.getFullYear() + 2, 1 -1);
        jQuery('#ritekhed-match-countdown').countdown({
            until: austDay
        });
        jQuery('#year').text(austDay.getFullYear());
    });

    //***************************
    // Fancybox Function
    //***************************
    jQuery(".fancybox").fancybox({
      openEffect  : 'elastic',
      closeEffect : 'elastic',
    });

    //***************************
    // Click to Top Button
    //***************************
    jQuery('.ritekhed-back-top').on("click", function() {
        jQuery('html, body').animate({
            scrollTop: 0
        }, 800);
        return false;
    });


});

jQuery('.progressbar1').progressBar({
    shadow : false,
    percentage : true,
    animation : true,
});

// Counter
var a = 0;
$(window).scroll(function() {

  var oTop = $('#counter').offset().top - window.innerHeight;
  if (a == 0 && $(window).scrollTop() > oTop) {
    $('.counter-value').each(function() {
      var $this = $(this),
        countTo = $this.attr('data-count');
      $({
        countNum: $this.text()
      }).animate({
          countNum: countTo
        },

        {

          duration: 5000,
          easing: 'swing',
          step: function() {
            $this.text(Math.floor(this.countNum));
          },
          complete: function() {
            $this.text(this.countNum);
            //alert('finished');
          }

        });
    });
    a = 1;
  }

});

//***************************
// FilterAble Function
//***************************
jQuery(window).on('load', function() {
    var $grid = $('.health-project-modren,.health-gallery-simple').isotope({
      itemSelector: '.element-item',
      layoutMode: 'fitRows'
    });
    // filter functions
    var filterFns = {
      // show if number is greater than 50
      numberGreaterThan50: function() {
        var number = $(this).find('.number').text();
        return parseInt( number, 10 ) > 50;
      },
      // show if name ends with -ium
      ium: function() {
        var name = $(this).find('.name').text();
        return name.match( /ium$/ );
      }
    };
    // bind filter button click
    $('.filters-button-group').on( 'click', 'a', function() {
      var filterValue = $( this ).attr('data-filter');
      // use filterFn if matches value
      filterValue = filterFns[ filterValue ] || filterValue;
      $grid.isotope({ filter: filterValue });
    });
    // change is-checked class on buttons
    $('.filters-button-group').each( function( i, buttonGroup ) {
      var $buttonGroup = $( buttonGroup );
      $buttonGroup.on( 'click', 'a', function() {
        $buttonGroup.find('.is-checked').removeClass('is-checked');
        $( this ).addClass('is-checked');
      });
    });
});

// When the window has finished loading create our google map below
google.maps.event.addDomListener(window, 'load', init);

function init() {
    // Basic options for a simple Google Map
    // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    var mapOptions = {
        // How zoomed in you want the map to start at (always required)
        zoom: 11,

        // The latitude and longitude to center the map (always required)
        center: new google.maps.LatLng(40.6700, -73.9400), // New York

        // How you would like to style the map. 
        // This is where you would paste any style found on Snazzy Maps.
        styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#444444"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#46bcec"},{"visibility":"on"}]}]
    };

    // Get the HTML DOM element that will contain your map 
    // We are using a div with id="map" seen below in the <body>
    var mapElement = document.getElementById('map');

    // Create the Google Map using our element and options defined above
    var map = new google.maps.Map(mapElement, mapOptions);

    // Let's also add a marker while we're at it
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(40.6700, -73.9400),
        map: map,
        title: 'Snazzy!'
    });
}