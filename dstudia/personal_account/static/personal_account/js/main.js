let animItems = document.querySelectorAll('.anim-item');
let docElem = document.documentElement;

function getElemTop(elem) {
    return window.pageYOffset + elem.getBoundingClientRect().top
}

if(animItems.length > 0) {
    window.addEventListener('scroll', addAnimClass);
}

function addAnimClass() {
    for(let item of animItems) {
        let itemPageTop = getElemTop(item);
        let windowAndScroll = window.pageYOffset + docElem.clientHeight;
        let itemCfStart = 3;
        let startingPoint = itemPageTop + (item.offsetHeight / itemCfStart);

        if(windowAndScroll > startingPoint) {
            item.classList.add('anim-active')
        }
    }
}