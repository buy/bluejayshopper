$(document).ready(function() {
  $('.dealrank').hide();
  $('.dealrank').slideDown(1500);
  $('.button, .dealrank, .backMain').mouseenter(function() {
    $(this).addClass('boxshadow');
  });
  $('.button, .dealrank, .backMain').mouseleave(function() {
    $(this).removeClass('boxshadow');
  });
  //  if mouse click, we show the DealRank intro div
  $('.dealrank').click(function() {
    $('.functionBox').toggle('slow', function() {
      $('.dealrank').slideToggle('slow');
      $('.dealrankIntro').slideToggle('slow');
      $('.backMain').slideToggle('slow');
    });
  });
  // go back to the main search page
  $('.backMain').click(function() {
    $('.functionBox').toggle('slow');
    $('.backMain').toggle('slow');
    $('.dealrankIntro').toggle('slow', function() {
       $('.dealrank').slideToggle('slow');
    });
  });  
});