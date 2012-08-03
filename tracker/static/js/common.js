var thisDomain = 'http://tracker.westiseast.co.uk';
var draggedItemID;
var draggedItem;

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
                var thisItem = 'li#'+data['date'];
                
                if ($(thisItem+' ul.jobslist').length) {
                    $(thisItem+' ul.jobslist').append(data['html']);
                } else {
                    $(thisItem).append('<ul class="jobslist"></ul>');
                    $(thisItem+' ul.jobslist').append(data['html']);
                    $('#add-form #loading').css('display', 'none');
                };
                $(thisItem+' a').unbind().bind('click', getDetails);
                bindDraggable($(thisItem+' a.draggable'));
                var thisDate = data['date'].split('-');
                loadStats(thisDate[1], thisDate[0]);
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
           var thisDate = $('#thisMonthYear').attr('date').split('-');
           loadStats(thisDate[0], thisDate[1]);   
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
                if (data == 'true') {$('#paid').addClass('paid');} else {$('#paid').removeClass('paid');} 
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

function loadStats(month, year) {
  $.ajax({
    url: '/load-stats/?year='+year+'&month='+month,
    method: 'GET',
    dataType: 'html',
    success: function(html) {
        $('#footer .inner').html(html);
    }
  });   
}

function loadJobs(month, year) {
  $.ajax({
    url: '/load-jobs/?year='+year+'&month='+month,
    method: 'GET',
    dataType: 'json',
    success: function(data) {

        $(data).each( function() {
           thisDay = 'li#'+this.date;
           thisList = thisDay+' ul.jobslist';
           thisItem = 'li#'+this.uid;
           itemHTML = '<li class="" id="'+this.uid+'"><a href="'+this.url+'" class="draggable '+this.cssclass+'">'+this.name+'</a></li>';
           
           
           
           if ($(thisList).length) {} else {
             $(thisDay).append('<ul class="jobslist droppable"></ul>');
             
           }

           $(thisList).append(itemHTML); 
           
           bindDraggable($(thisItem+' a.draggable'));
           
      		
      		
      		$('ul.droppable').droppable({
      			drop: function(event, ui) {
      			    ui.draggable.attr('style', '');
      			    var newLI = ui.draggable.parent().clone();
      			    ui.draggable.parent().remove();
      				$(this).append(newLI);
      				bindDraggable(newLI.children('a'));
      				newLI.children('a').bind('click', getDetails);
      				updateJob(newLI);
      			}
      		});
           
        });
        $('ul.jobslist li a').bind('click', getDetails); 
		
		
    }
  });
}

function bindDraggable(job) {
    $(job).draggable({
	    'opacity': 0.8,
	    'snap': true,
	    start: function(event, ui) {
	       $(job).unbind('click', false);
	    },
	    stop: function(event, ui) {
	       
	    },
	});    
}

function updateJob(job) {
   var newDate = job.parent().parent().attr('id');
   $.ajax({
      url: '/update-job/',
      type: 'POST',
      data: { date: newDate, uid: job.attr('id') },
      success: function() {
        // shoudl I do something here to celebrate moving a job? a message?  
      },
      error: function() {},
   });
}


/// a helper for CSRF protection in django when making ajax POSTs
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});



