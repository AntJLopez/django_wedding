/* global google, stripe, elements */

$(document).ready(() => {
  /*-----------------------------------------------------------------------------------*/
  /*  Smooth Scroll
  /*  Thanks to: https://github.com/davist11/jQuery-One-Page-Nav
  /*-----------------------------------------------------------------------------------*/

  function smoothScroll() {
    const formTarget = $('.rsvp-section');

    $('.nav').onePageNav({
      filter: ':not(.external)',
      scrollSpeed: 1500,
    });

    // Scrolls to form section
    $('.js-scroll').on('click', () => {
      $('html, body').animate(
        {
          scrollTop: formTarget.offset().top,
        },
        2000,
      );
      return false;
    });

    return false;
  }
  smoothScroll();

  /*-----------------------------------------------------------------------------------*/
  /*  Backstretch
  /*  Thanks to: http://srobbin.com/jquery-plugins/backstretch/
  /*-----------------------------------------------------------------------------------*/

  function backStrech() {
    $('aside').backstretch([
      '/static/img/placeholder-1.jpg',
      '/static/img/placeholder-2.jpg',

    ], { duration: 5000, fade: 1000 });
  }
  backStrech();

  /*-----------------------------------------------------------------------------------*/
  /*  Flexslider
  /*  Thanks to: http://www.woothemes.com/flexslider/
  /*-----------------------------------------------------------------------------------*/

  function flexSlider() {
    $('.flexslider').flexslider({
      animation: 'slide',
      slideshow: false,
      touch: true,
    });
  }

  flexSlider();

  /*-----------------------------------------------------------------------------------*/
  /*  Stripe Configuration
  /*-----------------------------------------------------------------------------------*/

  const stripeStyle = {
    base: {
      fontSize: '16px',
      color: '#32325d',
    },
  };

  const creditCard = elements.create('card', { stripeStyle });
  creditCard.mount('#gift-cc');
  let creditCardSection = 'Gifts';

  creditCard.addEventListener('change', ({ error }) => {
    let displayError;
    if (creditCardSection === 'Gifts') {
      displayError = $('#gift-cc-errors');
    } else {
      displayError = $('#rsvp-cc-errors');
    }
    if (error) {
      displayError.text(error.message);
    } else {
      displayError.text('');
    }
  });

  $(window).scroll(() => {
    const section = $('.side-nav li.active a').first().text();
    if (section === 'Gifts' && creditCardSection !== 'Gifts') {
      creditCard.unmount();
      $('.rsvp-error-child').remove();
      creditCard.mount('#gift-cc');
      creditCardSection = 'Gifts';
    } else if ($('#rsvp-cc').length > 0 && section === 'RSVP'
                                        && creditCardSection !== 'RSVP') {
      creditCard.unmount();
      $('.gift-error-child').remove();
      creditCard.mount('#rsvp-cc');
      creditCardSection = 'RSVP';
    }
  });

  /*-----------------------------------------------------------------------------------*/
  /*  Form Helper Functons
  /*-----------------------------------------------------------------------------------*/

  function populateErrors(errorField, errorArray, errorClass) {
    let i = 0;
    for (; i < errorArray.length; i += 1) {
      const newErrorField = errorField.clone();
      newErrorField.addClass(errorClass);
      newErrorField.text(errorArray[i]);
      errorField.after(newErrorField);
    }
  }

  /*-----------------------------------------------------------------------------------*/
  /*  Gift Form
  /*-----------------------------------------------------------------------------------*/

  function giftFormSubmit() {
    const formID = $('#gift_form'); // The ID of the gift form
    const url = formID.attr('action');

    formID.on('submit', async (e) => {
      e.preventDefault();
      const { token, error } = await stripe.createToken(creditCard);
      const errorElement = $('#gift-cc-errors');

      if (error) {
        errorElement.text(error.message);
      } else {
        errorElement.text('');

        const formData = formID.serializeArray();
        formData.push({ name: 'stripe_token', value: token.id });

        $.post(
          url,
          formData,
          (data) => {
            // Clear all existing errors
            $('.gift-error-child').remove();
            if ($.isEmptyObject(data.errors)) {
              $('#gift-success').foundation('reveal', 'open');
              formID.trigger('reset');
              creditCard.clear();
            } else {
              Object.keys(data.errors).forEach((key) => {
                function pushErrors(errorField) {
                  populateErrors(errorField, data.errors[key], 'gift-error-child');
                }
                if (key === 'first_name' || key === 'last_name' || key === 'email') {
                  pushErrors($('#gift-contact-errors'));
                } else if (key === 'amount') {
                  pushErrors($('#gift-amount-errors'));
                } else if (key === 'category_name') {
                  pushErrors($('#gift-category-errors'));
                } else if (key === 'gift_cc') {
                  pushErrors($('#gift-cc-errors'));
                }
              });
            }
          },
        );
      }
    });
  }
  giftFormSubmit();

  /*-----------------------------------------------------------------------------------*/
  /*  RSVP Form
  /*-----------------------------------------------------------------------------------*/

  function rsvpFormSubmit() {
    const formID = $('#rsvp_form');
    const url = formID.attr('action'); // eslint-disable-line

    formID.on('submit', async (e) => {
      e.preventDefault();

      const formData = formID.serializeArray();
      const data = {};
      $(formData).each((index, obj) => {
        data[obj.name] = obj.value;
      });
      data.attending = (data.attending === 'true');
      data.nights_onsite = parseInt(data.nights_onsite, 10);

      if (data.attending && data.nights_onsite > 0) {
        const { token, error } = await stripe.createToken(creditCard);
        const errorElement = $('#rsvp-cc-errors');

        if (error) {
          errorElement.text(error.message);
          return;
        }
        errorElement.text('');
        formData.push({ name: 'stripe_token', value: token.id });
      }

      $.post(
        url,
        formData,
        (data) => { // eslint-disable-line
          if ($.isEmptyObject(data.errors)) {
            $('#rsvp-success').foundation('reveal', 'open');
            formID.trigger('reset');
            creditCard.clear();
          } else {
            // formID.trigger('reset');
            // $('.checkbox').removeClass('checked');
          }
        },
      );
    });

    // Show/Hide RSVP Menu selection on accept/decline
    $('.decline').on('click', () => {
      $('.attending').fadeOut();
      $('.staying').fadeOut();
    });
    $('.accept').on('click', () => {
      $('.attending').fadeIn();
    });

    $('.onsite_0').on('click', () => {
      $('.staying').fadeOut();
    });
    $('.onsite_1, .onsite_2').on('click', () => {
      $('.staying').fadeIn();
    });
  }
  rsvpFormSubmit();

  /*-----------------------------------------------------------------------------------*/
  /*  DataTables
  /*-----------------------------------------------------------------------------------*/
  function prepareDatatable() {
    $('#guest_list').DataTable({
      paging: false,
      responsive: true,
      colReorder: true,
      fixedHeader: true,
    });
  }
  prepareDatatable();
});

/*-----------------------------------------------------------------------------------*/
/*  Google Map API
/*  Credit to: http://stiern.com/tutorials/adding-custom-google-maps-to-your-website/
/*-----------------------------------------------------------------------------------*/

let map;
const myLatlng = new google.maps.LatLng(42.279629, -73.072101); // Specify YOUR coordinates

const MY_MAPTYPE_ID = 'custom_style';

function initialize() {
  /*----------------------------------------------------------------------------*/
  /* Creates a custom color scheme for map
  /* For details on styling go to the link below:
  /* http://www.evoluted.net/thinktank/web-design/custom-google-maps-style-tool */
  /*----------------------------------------------------------------------------*/

  const featureOpts = [
    {
      featureType: 'road',
      stylers: [
        { hue: '#191970' },
        { gamma: 0.82 },
        { visibility: 'on' },
        { saturation: 62 },
        { lightness: -7 },
      ],
    },
    {
      featureType: 'poi',
      stylers: [
        { hue: '#f4d35e' },
        { lightness: 14 },
      ],
    },
    {
      stylers: [
        { hue: '#191970' },
      ],
    },
  ];

  const mapOptions = {
    zoom: 16,
    center: myLatlng,
    disableDefaultUI: true,
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, MY_MAPTYPE_ID],
    },
    mapTypeId: MY_MAPTYPE_ID,
  };

  map = new google.maps.Map(
    document.getElementById('map-canvas'),
    mapOptions,
  );

  const styledMapOptions = {
    name: 'Custom Style',
  };

  const customMapType = new google.maps.StyledMapType(
    featureOpts, styledMapOptions,
  );

  const image = new google.maps.MarkerImage(
    '/static/img/map-marker@2x.png',
    null,
    null,
    null,
    new google.maps.Size(55, 57),
  );

  // Includes custom marker on map
  const venueMarker = new google.maps.Marker({
    position: myLatlng,
    icon: image,
  });
  venueMarker.setMap(map);

  map.mapTypes.set(MY_MAPTYPE_ID, customMapType);
}

google.maps.event.addDomListener(window, 'load', initialize);
