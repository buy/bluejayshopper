$(document).ready(function() {
  $('.dealrank').hide().slideDown(1500);
  $('.button, .dealrank, .backMain').mouseenter(function() {
    $(this).addClass('boxshadow');
  })
  .mouseleave(function() {
    $(this).removeClass('boxshadow');
  });
  //  if mouse click, we show the DealRank intro div
  var dealInfo = $('.dealrankIntro');
  var backMain = $('.backMain');
  var functionBox = $('.functionBox');
  var dealrank = $('.dealrank');
  dealrank.click(function() {
    functionBox.toggle('slow', function() {
      dealrank.slideToggle('slow');
      dealInfo.slideToggle('slow');
      backMain.slideToggle('slow');
    });
  });
  // go back to the main search page
  backMain.click(function() {
    functionBox.toggle('slow');
    $(this).toggle('slow');
    dealInfo.toggle('slow', function() {
      dealrank.slideToggle('slow');
    });
  });  
});