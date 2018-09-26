/* global google */

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
  /*  RSVP Form Validation + Submission
  /*-----------------------------------------------------------------------------------*/

  function rsvpFormSubmit() {
    // this is the id of the form
    const formID = $('#js-form');

    // submits form with ajax method
    formID.on('submit', () => {
      $.ajax({
        url: 'mailer.php',
        type: 'POST',
        data: formID.serialize(), // serializes the form's elements.
        success(data) {
          $('.js-display')
            .addClass('message-panel')
            .html(data); // show response from the php script.
        },
      });

      return false; // avoid to execute the actual submit of the f
    });

    // Show/Hide RSVP Menu selection on accept/decline
    $('.decline').on('click', () => {
      $('.rsvp-meal-choice').fadeOut();
    });
    $('.accept').on('click', () => {
      $('.rsvp-meal-choice').fadeIn();
    });
  }
  rsvpFormSubmit();


  /*-----------------------------------------------------------------------------------*/
  /*  Gift Form
  /*-----------------------------------------------------------------------------------*/

  function giftFormSubmit() {
    const formID = $('#gift_form'); // The ID of the gift form
    const url = '/payments/make_gift/';

    formID.on('submit', (e) => {
      e.preventDefault();
      const formData = formID.serialize();

      $.post(
        url,
        formData,
        (data) => { // eslint-disable-line
        },
      );
    });
  }
  giftFormSubmit();

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
