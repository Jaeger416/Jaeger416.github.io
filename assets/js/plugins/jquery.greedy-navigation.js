/*
* Greedy Navigation
*
* http://codepen.io/lukejacksonn/pen/PwmwWV
*
*/

var $nav = $('#site-nav');
var $btn = $('#site-nav button');
var $vlinks = $('#site-nav .visible-links');
var $hlinks = $('#site-nav .hidden-links');

var breaks = [];

function updateNav() {
  // Re-measure all links so changes in viewport width or fonts cannot leave
  // links stranded in the overflow menu with stale width measurements.
  $hlinks.children().appendTo($vlinks);
  $btn.addClass('hidden');

  if ($vlinks.width() > $nav.width()) {
    $btn.removeClass('hidden');
    var availableSpace = $nav.width() - $btn.outerWidth() - 30;
    while ($vlinks.width() > availableSpace && $vlinks.children().length > 1) {
      $vlinks.children().last().prependTo($hlinks);
    }
  }

  var hiddenCount = $hlinks.children().length;
  $btn.attr('count', hiddenCount);
  if (hiddenCount === 0) {
    $btn.addClass('hidden');
    $hlinks.addClass('hidden');
  }
}

// Window listeners

$(window).resize(function() {
  updateNav();
});

$btn.on('click', function() {
  $hlinks.toggleClass('hidden');
  $(this).toggleClass('close');
});

updateNav();