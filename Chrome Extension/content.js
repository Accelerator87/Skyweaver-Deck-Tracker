chrome.runtime.onMessage.addListener( function( msg, sender, callback ) {
 	"use strict";

    if( msg.text === 'report_back' ) {

        var resultDOM = getContent( document );
        callback( resultDOM );

    }

});

function getContent( docDOM ) {
 	"use strict";

	var cloneDOM = docDOM.cloneNode(true);
	var framesDoc = docDOM.getElementsByTagName('iframe');
	var framesClone = cloneDOM.getElementsByTagName('iframe');

	if( framesClone.length > 0 ) {

		for( var i = 0; i < framesClone.length; i++ ) {

			try {

				var newContent = framesDoc[i].contentDocument;
				var divWrap = document.createElement('div');
				divWrap.id = framesDoc[i].id;
				divWrap.style.cssText = framesDoc[i].style.cssText;
				divWrap.className = framesDoc[i].className + ' original_iframe';
				if( framesDoc[i].width!=='' && divWrap.style.width==='' ) { divWrap.style.width = framesDoc[i].width + 'px'; }
				if( framesDoc[i].height!=='' && divWrap.style.height==='' ) { divWrap.style.height = framesDoc[i].height + 'px'; }
				divWrap.innerHTML = getContent( newContent );
				framesClone[i].outerHTML = divWrap.outerHTML;

			} catch( exception ) {

				// Return Original iFrame HTML

			}

		}

	}
	return cloneDOM.all[0].outerHTML;

}

