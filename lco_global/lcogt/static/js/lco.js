//dynamically create and size all rays from locations to corresponding info boxes
function mapArrows () {
    $('.arrow').each(function () {
        $(this).css({'border': 'none', 'margin': '0px'});
        var originPad = 7;  //The dots aren't really centered on their locations
        var borderColor = "rgba(255,203,8,0.4)";
        var borders = {'top': 'none', 'right': 'none', 'bottom': 'none', 'left': 'none'};
        //var offset = [$('.worldMap').offset().top, $('.worldMap').offset().left];
        //GET THE POSITION OF THE CIRCLE X,Y
        var origin = [$(this).offset().left + originPad, $(this).offset().top + $(window).scrollTop() + originPad];
        //FIND THE CORRESPONDING INFO BOX
        var location = $(this).data('location');
        //console.log(location);
        var $dataBox = $("." + location + " .infoBox");
        //MAP THE DATA BOX UPPER LEFT X,Y AND LOWER RIGHT X,Y
        var points = [$dataBox.offset().left, $dataBox.offset().top];
        points.push(points[0] + $dataBox.width(), points[1] + $dataBox.height());
        //console.log(origin);
        //console.log(points);
        //QUICK N' DIRTY CALCULATION OF THE SIZE AND SHAPE OF EACH ARROW
        //DIFFERENT CALCS DEPENDING ON WHICH SIDE THE INFO BOX IS ON
        switch($(this).data('direction')) {
            case ('up'):
                borders = {
                    'top':  (origin[1] - points[3]) + 'px solid ' + borderColor,
                    'right': (points[2] - origin[0]) + 'px solid transparent',
                    'bottom': 'none',
                    'left': (origin[0] - points[0]) + 'px solid transparent'
                };
                //console.log(borders);
                //console.log("up!");
                var marginFix = (points[3] - origin[1] + originPad) + 'px 0px 0px ' + (points[0] - origin[0] + originPad) + 'px';

                break;
            case ('right'):
                borders = {
                    'top': (origin[1] - points[1]) + 'px solid transparent',
                    'right': (points[0] - origin[0]) + 'px solid ' + borderColor,
                    'bottom': (points[3] - origin[1]) + 'px solid transparent',
                    'left': 'none'
                };
                //console.log(borders);
                //console.log("right!");
                var marginFix = (points[1] - origin[1] + originPad) + 'px 0px 0px ' + originPad + 'px';

                break;
            case ('down'):
                borders = {
                    'top': 'none',
                    'right': (points[2] - origin[0]) + 'px solid transparent',
                    'bottom': (points[1] - origin[1]) + 'px solid ' + borderColor,
                    'left': (origin[0] - points[0]) + 'px solid transparent'
                };
                //console.log(borders);
                //console.log("down!");
                var marginFix = originPad + 'px 0px 0px ' + (points[0] - origin[0] + originPad) + 'px';

                break;
            case ('left'):
                borders = {
                    'top': (origin[1] - points[1]) + 'px solid transparent',
                    'right': 'none',
                    'bottom': (points[3] - origin[1]) + 'px solid transparent',
                    'left': (origin[0] - points[2]) + 'px solid ' + borderColor
                };
                //console.log(borders);
                //console.log("left!");
                var marginFix = (points[1] - origin[1] + originPad) + 'px 0px 0px ' + (points[2] - origin[0] + originPad) + 'px';

                break;
        }
        //FINALLY, APPLY ALL THAT CSS WE'VE BEEN MATHING UP.
        $(this).css({
            'border-top': borders.top,
            'border-right': borders.right,
            'border-bottom': borders.bottom,
            'border-left': borders.left,
            'margin': marginFix
        });
        //console.log(borders);
    });
}

function posMobileBox () {
    if ($( window ).width() < 768) {
        $(".infoBox").each(function () {
            var boxWidth = $(this).width();
            var leftPos = ($( window ).width() - boxWidth) / 2;
            //console.log(leftPos);
            $(this).css('left', leftPos + 'px');
        });
    } else {
        $('.infoBox').css('left', '');
    }
}

//Temporary javascript solution to place images on down pages.
//Since JS can't read directory contents, you need to know how many images there are ahead of time.
//You also need to have a consistent naming scheme.
//This should be replaced by a backend image randomizer, 
//or an AJAX response from a simple server-side script.
/*function placeImgs (available, numImg, target) {
    var imgArray = [];
    console.log(available);
    console.log($(target));
    var path = "images/headerImg/";
    for (var i = 1; i <= available; i++) {
        imgArray[i - 1] = path + "HeaderPic-" + i + ".jpg";
        console.log(imgArray[i-1]);
    }
    imgArray = shuffle(imgArray);
    for (var j = 0; j < numImg; j++) {
        $(target).append('<img src="' + imgArray[j] + '" />');
    }
}

// Shamelessly stolen from StackOverflow
function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}*/

$( document ).ready(function() {
    //Display or hide all locations at once
    $('.displayBox').click(function() {
    	if ($(this).hasClass('shown')) {
    		$(this).removeClass('shown');
            $(this).text('Show Entire Network');
    		$('.location').each(function() {
    			$(this).removeClass('shown');
    		});
            $('.arrow').each(function() {
                $(this).removeClass('shown');
            });
    	} else {
    		$(this).addClass('shown');
            $(this).text('Hide Entire Network');
    		$('.location').each(function() {
    			$(this).addClass('shown');
    		});
            $('.arrow').each(function() {
                $(this).addClass('shown');
            });
    	}
    });
    //INFO BOX IS CSS-ONLY, BUT ARROW/RAY IS SEPERATE ELEMENT.  LET'S FIX THAT:
    $('.location').each(function () {
        $(this).hover(function () {
            $('.' + $(this).data('location')).addClass('shown');
        }, function() {
            $('.' + $(this).data('location')).removeClass('shown');
        });
    });

    mapArrows();
    posMobileBox();
    //WATCH FOR WINDOW RESIZING AND ADJUST THE ARROWS/RAYS, ALSO DYNAMICALLY POSITION INFO BOXES FOR MOBILE
    $( window ).resize(function() {
        mapArrows();
        posMobileBox();
    });
});

$(window).on("load", function() {
  mapArrows();
  posMobileBox();
});