/* global google, stripe, elements */

$(document).ready(() => {
  /*-----------------------------------------------------------------------------------*/
  /*  Smooth Scroll
  /*  Thanks to: https://github.com/davist11/jQuery-One-Page-Nav
  /*-----------------------------------------------------------------------------------*/

  function smoothScroll() {
    const formTarget = $('.js-form'); // Assign this class to corresponding section on Index.html    $('.nav').onePageNav({

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
      $('#rsvp-cc-errors').text('');
      creditCard.mount('#gift-cc');
      creditCardSection = 'Gifts';
    } else if (section === 'RSVP' && creditCardSection !== 'RSVP') {
      creditCard.unmount();
      $('#gift-cc-errors').text('');
      creditCard.mount('#rsvp-cc');
      creditCardSection = 'RSVP';
    }
  });

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
          (data) => { // eslint-disable-line
            if ($.isEmptyObject(data.errors)) {
              $('#gift-display').text('Success!').addClass('message-panel');
              formID.trigger('reset');
              creditCard.clear();
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

    // formID.on('submit', async (e) => {
    //   e.preventDefault();
    //   // const { token, error } = await stripe.createToken(rsvpCC);
    //   // const errorElement = $('#rsvp-cc-errors');
    //
    //   if (false) { // eslint-disable-line no-constant-condition
    //     // errorElement.text(error.message);
    //   } else {
    //     // errorElement.text('');
    //
    //     const formData = formID.serializeArray();
    //     // formData.push({ name: 'stripe_token', value: token.id });
    //
    //     $.post(
    //       url,
    //       formData,
    //       (data) => { // eslint-disable-line
    //         if ($.isEmptyObject(data.errors)) {
    //           formID.trigger('reset');
    //           rsvpCC.clear();
    //         }
    //       },
    //     );
    //   }
    // });
  }
  // Show/Hide RSVP Menu selection on accept/decline
  $('.decline').on('click', () => {
    $('.attending').fadeOut();
    $('.staying.').fadeOut();
  });
  $('.accept').on('click', () => {
    $('.attending').fadeIn();
  });

  $('.onsite_0').on('click', () => {
    console.log('NOT STAYING');
    $('.staying').fadeOut();
  });
  $('.onsite_1, .onsite_2').on('click', () => {
    console.log('STAYING');
    $('.staying').fadeIn();
  });
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
