$(function()
{	
    var docTop = $(document).scrollTop();
    var header = $('.headline').outerHeight();

    $(window).scroll(function() 
    {
        var in_top = $(document).scrollTop();

        if (in_top > header)
        {
        	$('.headline').addClass('g');
        	//$(".headline").slideUp();
        } 
        else 
        {
        	$('.headline').removeClass('g');
        	//$(".headline").slideDown();
        }

        if (in_top > docTop)
        {
        	$('.headline').removeClass('s');
        } 
        else 
        {
        	$('.headline').addClass('s');        	
        }				

        docTop = $(document).scrollTop();	
    });
});
$(document).ready(function()
{
	$(".headline").click(function()
	{
		$(".area1").slideToggle("slow");			
	});
});