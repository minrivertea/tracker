var thisDomain = 'http://tracker.westiseast.co.uk';


function addJob() {
   var date = $(this).attr('id');
   if ($(this).hasClass('selected')) {
      $('#add-form').css({'display': 'none', 'top': '0' });
      $(this).removeClass('selected');
   } else {
      clearAll();
      $('li').removeClass('selected');
      $(this).addClass('selected');
      $('#add-form').css({'display': 'block', 'top': '40%', 'left': '30%'});
      $('#add-form input:text:visible:first').focus();
      $('#add-form input#id_start_date').val(date);
      $('#add-form').unbind();
      $('#add-form').bind('submit', saveJob);
   }    
}

function saveJob() {
      $(this).css('opacity', '0.5');
      $('#add-form #loading').css('display', 'block');
      $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            type: "POST",
            success: function(data) {
                clearAll();
                if ($('li#'+data['date']+' ul.jobslist').length) {
                    $('li#' + data['date'] + ' ul.jobslist').append(data['html']);
                } else {
                    $('li#'+data['date']).append('<ul class="jobslist"></ul>');
                    $('li#'+data['date']+' ul.jobslist').append(data['html']);
                    $('li#'+data['date']+' a.link').unbind().bind('click', getDetails);
                    $(this).css('opacity', '1');
                    $('#add-form #loading').css('display', 'none');
                }  
            } 
      });
      return false;
}

function deleteJob() {
     $.ajax({
        url: $(this).attr('href'),
        success: function(data) {
           clearAll();
           $('li#'+ data).remove();   
        }
     });
     return false;   
}

function getDetails(e) {
   
   var posX = e.pageX;
   var posY = e.pageY;
   var height = $(window).height();
   var width = $(window).width();
   var cssClass = 'popout-inner';
   if ((width-posX) < 500) {
      cssClass += ' left';
   }
   if ((height-posY) < 500) {
      cssClass += ' top';
   } 
   
   if ($(this).hasClass('selected')) {
        $('.popout').remove();
        $('li span.link').removeClass('selected');
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
               $('a#delete').bind('click', deleteJob);
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
                if (data == 'true') {$('#done').addClass('done');} else {$('#done').removeClass('done');}
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
                if (data == 'true') {$('#paid').addClass('done');} else {$('#paid').removeClass('done');} 
            }
        });
        return false;
    });
}

var shareURL;

function makeURL() {
   if ($('#sharelink').text() == thisDomain) {
        $.ajax({
         url: '/url/make/',
         type: "GET",
         success: function(data) {
            shareURL = data;
            $('#sharelink').append(data); 
         }
      }); 
      return false;
   } else {}
}
 

function expandHeader(block) {
   var currentBlock = $('#'+block);
   if ($('#expandable').hasClass('open')) {
      if (currentBlock.hasClass('selected')) {
         $('#expandable').removeClass('open');
         $('#header a').removeClass('selected');
      } else { 
         $('#header a').removeClass('selected');
         currentBlock.addClass('selected');
         getHeaderContents(block);
      }
      
   }
   
   else {
      $('#expandable').addClass('open');
      currentBlock.addClass('selected');
      getHeaderContents(block);
   }
   
   
}

function getHeaderContents(block) {
  if (block == 'share') {
     makeURL(); 
  }   
  
  if (block == 'user') {
    
  }
}


function expandFooter() {
  if ($('#footer').hasClass('expanded')) {
      $('#footer').css('height', '40px');
      $('#footer').removeClass('expanded');  
  } else {
      $('#footer').css('height', '300px');
      $('#footer').addClass('expanded');     
  } 
}



