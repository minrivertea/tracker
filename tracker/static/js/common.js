var thisDomain = 'http://tracker.westiseast.co.uk';
var draggedItemID;
var draggedItem;
var tD = '';
var mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
var dim=[31,0,31,30,31,30,31,31,30,31,30,31];
var dow=['Mon','Tue','Wed','Thu','Fri','Sat', 'Sun'];
var today= new Date();


function buildCal() {
    
    if (tD.length==0) { tD = new Date() } else { tD = tD }
    y = tD.getFullYear();
    m = tD.getMonth()+1;      
    
    var oD = new Date(y, m-1, 1);
    oD.fd=((oD.getDay()-1<0))?6:oD.getDay()-1; 
             
    dim[1]=(((oD.getFullYear()%100!=0)&&(oD.getFullYear()%4==0))||(oD.getFullYear()%400==0))?29:28; 
    
    var t='';
    for (i=0;i<=36;i++) {
                
        var x= ((i-oD.fd>=0)&&(i-oD.fd<dim[m-1]))?i-oD.fd+1 : '';
        var cssclass = '';
        
        if (x == '') cssclass+= 'noday';
        if ((y==today.getFullYear()) && (m-1==today.getMonth()) && (x==today.getDate())) cssclass+='today ';
        
        t+='<li id="'+y+'-'+m+'-'+x+'" class="'+cssclass+'"><h3 class="inner_day">'+x+'</h3><ul class="jobslist droppable"></ul></li>';
        
    }
    $('#month').html(t);
    $('#thisMonthYear').html(mn[m-1]+' '+y);
    loadJobs(m, y);
    loadStats();
    $('#month li').not('.noday').bind('click', addJob);
    $('.noday').bind('click', clearAll);
}


function addJob() {
   if ($(this).hasClass('selected')) {
      $('#add-form').css({'display': 'none',});
      $(this).removeClass('selected');
   } else {
      clearAll();
      $(this).addClass('selected');
      $('#add-form').css({'display': 'block',});
      $('#add-form input:text:visible:first').focus();
      $('#add-form input#id_start_date').val($(this).attr('id'));
      $('#add-form').bind('submit', saveJob);
   }    
}

function saveJob() {
      $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: "json",
            type: "POST",
            success: function(data) {
                clearAll();
                html = '<li id="'+data.hashkey+'"><a href="'+data.url+'" class="draggable">'+data.name+'</a></li>';
                $('li#'+data.date+' ul.jobslist').append(html);
                $('li#'+data.hashkey+' a').unbind().bind('click', getDetails);
                bindDraggable();
                loadStats();
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
           loadStats();   
        }
     });
     return false;   
}

function getDetails(e) {
   
   var cssClass = 'popout-inner';
   if (($(window).width()-e.pageX) < 500) {
      cssClass += ' left';
   }
   if (($(window).height()-e.pageY) < 500) {
      cssClass += ' top';
   } 
      
   clearAll();
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




function loadJobs(month, year) {
  $.ajax({
    url: '/load-jobs/?year='+year+'&month='+month,
    method: 'GET',
    dataType: 'json',
    success: function(data) {
        $(data).each( function() {
           html = '<li class="" id="'+this.uid+'"><a href="'+this.url+'" class="draggable '+this.cssclass+'">'+this.name+'</a></li>';
           $('li#'+this.date+' ul.jobslist').append(html); 
        });
        
        $('ul.jobslist li a').each(function(){
            $(this).unbind().bind('click', getDetails); 
        });	
        bindDraggable();
        bindDroppable();
    }
  });     	
}

function bindDraggable() { 
    $('.draggable').draggable({
       'opacity': 0.8,
	   'snap': true,
	   start: function(event, ui) {
	       $(this).unbind('click', false);
	   }
     });
}

function bindDroppable() {
    $('.droppable').droppable({
		drop: function(event, ui) {
		    var newLI = ui.draggable.parent().clone();
		    ui.draggable.parent().remove();
			$(this).append(newLI);
			newLI.children('a').attr('style', '');
			bindDraggable(newLI.children('a'));
			newLI.children('a').unbind().bind('click', getDetails);
			updateJob(newLI);
			
		}
    });    
}


function updateJob(job) {
   var nD = job.parent().parent().attr('id');
   $.ajax({
      url: '/update-job/',
      type: 'POST',
      data: { date: nD, uid: job.attr('id') },
      success: function() {
        // shoudl I do something here to celebrate moving a job? a message?  
      },
      error: function() {},
   });
}





function nextMonth(e) {
        
    if (tD.getMonth() == 11) {
        nD = new Date(tD.getFullYear() + 1, 0, 1);
    } else {
        nD = new Date(tD.getFullYear(), tD.getMonth() + 1, 1);
    }
        
    tD = nD;
    buildCal();
    e.preventDefault();
}


function prevMonth(e) {
        
    if (tD.getMonth() == 0) {
        nD = new Date(tD.getFullYear() - 1, 11, 1);
    } else {
        nD = new Date(tD.getFullYear(), tD.getMonth() - 1, 1);
    }
    
    tD = nD;
    buildCal();
    e.preventDefault();
}

function loadStats() {
   $('#footer').load('/load-stats/?year='+tD.getFullYear()+'&month='+(tD.getMonth()+1));
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



