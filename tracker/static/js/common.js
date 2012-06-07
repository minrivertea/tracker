function addJob() {
   var date = $(this).attr('id');
   if ($(this).hasClass('selected')) {
      $('#add-form').css({'display': 'none', 'top': '0' });
      $(this).removeClass('selected');
   } else {
      clearAll();
      $('td').removeClass('selected');
      $(this).addClass('selected');
      $('#add-form').css({'display': 'block', 'top': '40%', 'left': '35%'});
      $('#add-form input:text:visible:first').focus();
      $('#add-form input#id_start_date').val(date);
   }    
}

function getDetails(e) {
   
   var posX = e.pageX;
   var posY = e.pageY;
   var height = $(window).height();
   var width = $(window).width();
   var cssClass = 'popout-inner';
   if ((width-posX) < 400) {
      cssClass += ' left';
   }
   if ((height-posY) < 300) {
      cssClass += ' top';
   } 
   
   if ($(this).hasClass('selected')) {
        $('.popout').remove();
        $('td span.link').removeClass('selected');
   } else {
        clearAll();
        $(this).addClass('selected');
        $(this).parent().prepend('<div class="popout"><div class="'+cssClass+'"><img id="loading" src="/static/images/loading.gif"></div></div>');
        $.ajax({
            url: $(this).attr('href'),
            cache: false,
            success: function(data) {
               $('.popout-inner').html(data);
               $('#loading').css('display', 'none');
               jobDone();
               jobPaid();
            }
        });
   }
   e.preventDefault();
   e.stopPropagation();
   e.stopImmediatePropagation();    
}

function clearAll() {
  $('.popout').remove();
  $('#add-form').css({'display': 'none', 'top': '0' });
  $('.selected').removeClass('selected'); 
}




function jobDone() {
    $('a#done').click( function() {
        $.ajax({
            url: $(this).attr('href'),
            success: function(data) {
                if (data == 'true') {$('#done').addClass('done');}   
            }
        });
        return false;
    });
}

function jobPaid() {
    $('a#paid').click( function() {
        $.ajax({
            url: $(this).attr('href'),
            success: function(data) {
                if (data == 'true') {$('#paid').addClass('done');}   
            }
        });
        return false;
    });
}


