let openers = document.querySelectorAll('.opener');
let closers = document.querySelectorAll('.closer');




function openPopup(event) {
    event.preventDefault();
    let popup = this.nextElementSibling;
    console.log(popup)
    if(!popup.classList.contains('open')){
        popup.classList.add('open');
    }
}

function closePopup(event) {
    event.preventDefault();
    let popup = this.closest('.popup')
    if(popup.classList.contains('open')){
        popup.classList.remove('open');
    }
}

if(openers.length > 1) {
    for(opener of openers) {
        opener.addEventListener('click', openPopup);
    }
} else {
    openers[0].addEventListener('click', openPopup)
}

if(closers.length > 1) {
    for(closer of closers) {
        closer.addEventListener('click', closePopup);
    }
} else {
    closers[0].addEventListener('click', closePopup)
}


