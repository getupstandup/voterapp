var mymap;

function saveEmail () {
  email = $('#email').val();
  $.post('/save-email', { email: email }, function (data) {
    alert('Email address saved successfully.');
  })
  return false;
}

$(function() {
  $('.question-list li').click(function () {
    $(this).toggleClass('active');
  })

  $('#question-confirm').click(function () {
    var answers = [];
    $.each($('.question-list li.active'), function (idx, obj) {
      answers.push($(obj).data('id'));
    });

    if (answers.length == 0) {
      alert('Please select at least one option.');
      return false;
    }

    $.post('/question-confirm', { answer: answers }, function (data) {
      $('.sec-address').removeClass('d-none');      
      location.href = '/#id-sec-address';
      autocomplete = new google.maps.places.Autocomplete((document.getElementById('address')),
                    {types: ['geocode']});

    })
  })

  $('#address-confirm').click(function () {
    var address = $('#address').val().trim();

    if (address == '') {
      alert('Please enter the address where you are registered to vote.');
      return false;
    }

    $.post('/address-confirm', { address: address }, function (data) {
      if (data == 'fail') {
        alert('Something went wrong. Please check the address and enter it again.');
      } else {
        $('.sec-map').removeClass('d-none');
        $('.rep_name').html('Your representative is: '+data.rep_name);        
        location.href = "/#id-sec-address";

        if (mymap != undefined) { 
          mymap.off();
          mymap.remove(); 
        } 

        mymap = L.map('mapid').setView(data.location, 12);
        L.tileLayer('https://api.mapbox.com/styles/v1/mrlafranchi/cjed32lr92bzc2smw9afeka1t/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibXJsYWZyYW5jaGkiLCJhIjoiY2pneTJpdWUyMTRicTJxbDZnd3V6aWN3YSJ9.PKJe-IBFB8JAJhFsbsXE1w', {
          attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
          maxZoom: 18,
          id: 'mapbox.streets',
          accessToken: 'pk.eyJ1IjoibXJsYWZyYW5jaGkiLCJhIjoiY2pneTJpdWUyMTRicTJxbDZnd3V6aWN3YSJ9.PKJe-IBFB8JAJhFsbsXE1w'
        }).addTo(mymap);

        L.marker(data.location).addTo(mymap);

        for (ii in data.polygon) {
          L.polygon(data.polygon[ii]).addTo(mymap);
        }
      }
    })
  })

  $('#show-chart').click(function () {
    $.post('/chart-data', function (data) {
      $('.sec-chart').removeClass('d-none');
      location.href = '/#id-sec-chart';

      var chartColors = window.chartColors;
      var color = Chart.helpers.color;
      var config = {
        data: {
          datasets: [{
            data: data.selected,
            backgroundColor: [
              color(chartColors.red).alpha(0.5).rgbString(),
              color(chartColors.orange).alpha(0.5).rgbString(),
              color(chartColors.yellow).alpha(0.5).rgbString(),
              color(chartColors.purple).alpha(0.5).rgbString(),
              color(chartColors.blue).alpha(0.5).rgbString(),
            ],
            label: 'My dataset' // for legend
          }],
          labels: data.labels
        },
        options: {
          tooltips: {
            callbacks: {
              label: function(tooltipItem, data) {
                return data.labels[tooltipItem.index]+': '+tooltipItem.yLabel+'%';
              }
            }
          },
          responsive: true,
          legend: {
            position: 'bottom',
            labels: {
              padding: 20
            }
          },
          title: {
            display: true,
            fontSize: 16,
            padding: 20,
            text: 'This is how the voters in you district voted.'
          },
          scale: {
            ticks: {
              beginAtZero: true,
              callback: function (ax) {
                return ax + '%';
              }
            },
            reverse: false
          },
          animation: {
            animateRotate: false,
            animateScale: true
          }
        }
      };

      var ctx = document.getElementById('chart-area');
      if ($(window).width() < 768) {
        ctx.height = 300;
      }
      Chart.PolarArea(ctx, config);
    })
  })
})
