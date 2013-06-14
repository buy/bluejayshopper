$(document).ready(function() {
    $('#content').fadeOut(0)
    $('#content').fadeIn(1200);
    $('.merchantimg').fadeTo(0, 0.5);
    // Click to show the search box
    $('.slide').mouseenter(function() {
      $(this).addClass('boxshadow');
    });
    $('.slide').mouseleave(function() {
      $(this).removeClass('boxshadow');
    });
    $('.slide').click(function() {
        $('.slide').toggle(1000);
        //$('.slide').effect('clip');
        $('.search-box').slideToggle('slow');
        //$('.slide').effect('clip');
    });
		// For zebra striping 
    $("table tr:nth-child(odd)").addClass("odd-row");
		// For cell text alignment 
		$("table td:first-child, table th:first-child").addClass("first");
		// For removing the last border
		$("table td:last-child, table th:last-child").addClass("last");
    // Highlight 
    $('a').mouseover(function(){
        $(this).addClass('textshadow');
    })
    $('a').mouseout(function(){
        $(this).removeClass('textshadow');
    });
    // fadeIn and fadeOut on Click to Buy
    $('tr').mouseenter(function() {
      $(this).find('.merchantimg').fadeTo(600, 1);
    });
    $('tr').mouseleave(function() {
      $(this).find('.merchantimg').fadeTo(600, 0.5);
    });

    $('a').click(function(){
        var link = null;
        link = $(this).attr("href");
        link = encodeURIComponent(link);      
        $.get("/click?link=" + link);
    });
});


