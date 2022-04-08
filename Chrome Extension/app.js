function renderStatus(statusText) {
	"use strict";
	document.getElementById('status').innerHTML = statusText;
}

function getCurrentTab( callback ) {
	"use strict";

	var queryInfo = {
		active: true,
		currentWindow: true
	};

	chrome.tabs.query( queryInfo, function( tabs ) {
		var tab = tabs[0];
		callback( tab );
	});

}

function get_deck_content ( DOMcontent ) {

	var regex1 = /class="horizon-text css-10f5hy5 egbwoy00">([A-Za-z\s]+)</;
    var regex2 = /data-card-row-id="([0-9]+)"/g;
    var regex3 = /<img src="(.+)" class="prismIcon"/;
    var regex4 = /icons\/([A-Z]+).png/;
    var regex5 = /class="horizon-text css-1xqtx3h egbwoy00">([A-Za-z0-9]+)</;

	var deckName = regex1.exec(DOMcontent)[1];
    var cardsID  = regex2.exec(DOMcontent);
	var heroName = regex4.exec(regex3.exec(DOMcontent)[1])[1];
	var copyStr  = regex5.exec(DOMcontent)[1];
	var heroIcon = heroName + '-hero.jpeg';
 	
	if ( (deckName == null) || (cardsID == null) || (heroName == null) || (heroIcon == null) || (copyStr == null) ) {
		document.getElementById('status').className = 'error';
		renderStatus( 'Please refresh page and press setting bottom on the deck you want to copy.' );
		return;
	}

	if ( (deckName == undefined) || (cardsID == undefined) || (heroName == undefined) || (heroIcon == undefined) || (copyStr == undefined) ) {
		document.getElementById('status').className = 'error';
		renderStatus( 'Please refresh page and press setting bottom on the deck you want to copy.' );
		return;
	}

	if ( (deckName == "") || (cardsID == "") || (heroName == "") || (heroIcon == "") || (copyStr == "") ) {
		document.getElementById('status').className = 'error';
		renderStatus( 'Please refresh page and press setting bottom on the deck you want to copy.' );
		return;
	}
	
    var role = '';
	switch (heroName) {
	  	case 'STR': { heroName = 'Ada'   ;  role = 'Strength'           ;  break; };
	  	case 'AGY': { heroName = 'Samya' ;  role = 'Agility'            ;  break; };
	  	case 'WIS': { heroName = 'Lotus' ;  role = 'Wisdom'             ;  break; };
	  	case 'HRT': { heroName = 'Bouran';  role = 'Heart'              ;  break; };
	  	case 'INT': { heroName = 'Ari'   ;  role = 'Intellect'          ;  break; };
	  	case 'STA': { heroName = 'Fox'   ;  role = 'Strength Agility'   ;  break; };
	  	case 'STW': { heroName = 'Titus' ;  role = 'Strength Wisdom'    ;  break; };
	  	case 'STH': { heroName = 'Horik' ;  role = 'Strength Heart'     ;  break; };
	  	case 'STI': { heroName = 'Mira'  ;  role = 'Strength Intellect' ;  break; };
	  	case 'AGW': { heroName = 'Iris'  ;  role = 'Agility Wisdom'     ;  break; };
	  	case 'HRA': { heroName = 'Zoey'  ;  role = 'Agility Heart'      ;  break; };
	  	case 'AGI': { heroName = 'Mai'   ;  role = 'Agility Intellect'  ;  break; };
	  	case 'HRW': { heroName = 'Axel'  ;  role = 'Wisdom Heart'       ;  break; };
	  	case 'INW': { heroName = 'Banjo' ;  role = 'Wisdom Intellect'   ;  break; };
	  	case 'HRI': { heroName = 'Sitti' ;  role = 'Heart Intellect'    ;  break; };
	 	default: { break; };
	};

	var deckInfo = {
		'deckName' : deckName,
		'copyStr'  : copyStr,
		'heroName' : heroName,
		'heroIcon' : heroIcon,
		'role'     : role,
	};

	var str = deckName + "\n" + copyStr + "\n" + heroName + "\n" + role + "\n";
	var cnt = 1;
    while (cardsID != null) {
	    deckInfo['card'+cnt.toString()] = cardsID[1];
	    str += cardsID[1].toString() + " , ";
	    cardsID = regex2.exec(DOMcontent);
	    cnt = cnt + 1;
    }

    renderStatus( str);

	return;


}


document.addEventListener('DOMContentLoaded', function() {
	"use strict";

	getCurrentTab( function( tab ) {
		
		renderStatus( 'Loading Your Deck...' );

		chrome.tabs.sendMessage( tab.id, {text: 'report_back'}, function( DOMcontent ) { 

			if( DOMcontent !== undefined ) {

				get_deck_content(DOMcontent);
				//renderStatus( 'Success' );

			} else {

				document.getElementById('status').className = 'error';
				renderStatus( 'Please refresh page' );
			}

		});

	});

});

