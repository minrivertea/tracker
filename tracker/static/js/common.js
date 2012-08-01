var thisDomain = 'http://tracker.westiseast.co.uk';


function addJob() {
   var date = $(this).attr('id');
   if ($(this).hasClass('selected')) {
      $('#add-form').css({'display': 'none',});
      $(this).removeClass('selected');
   } else {
      clearAll();
      $('li').removeClass('selected');
      $(this).addClass('selected');
      $('#add-form').css({'display': 'block',});
      $('#add-form input:text:visible:first').focus();
      $('#add-form input#id_start_date').val(date);
      $('#add-form').unbind();
      $('#add-form').bind('submit', saveJob);
   }    
}

function saveJob() {
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
      
   
   // if it's already open, close it
   if ($(this).hasClass('selected')) {
        clearAll();
   } 
   
   // if it's not open, then open the popout
   else {
        
        clearAll(); // close any other popouts
        $(this).addClass('selected'); // select this
        
        // if it's already been loaded previously, don't load the ajax again, just make it visible
        if ($(this).parent().children('.popout').length) {
            $(this).parent().children('.popout').css('display', 'block');
        } 
        
        
        else {
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
   }
   e.preventDefault();
   e.stopPropagation();
   e.stopImmediatePropagation();    
}



function clearAll() {
  $('.popout').css('display', 'none');
  $('#add-form').css({'display': 'none', 'top': '0' });
  $('.selected').removeClass('selected');
  $('#expandable').attr('class', '');
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
     $('#share-full').css('display', 'block');
     $('#user-full').css('display', 'none');
     makeURL(); 
  }   
  
  if (block == 'user') {
    $('#share-full').css('display', 'none');
     $('#user-full').css('display', 'block');
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



