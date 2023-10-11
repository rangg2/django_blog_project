// 공통으로 사용되는 기능
//사이드 메뉴바
const menu = document.getElementById("moblie-nav");
//사이드 메뉴바가 열려있는지 여부
let isOpen = menu.classList.contains("display_none") ? false : true;

function menuOpen() {
    if (isOpen) {
        menu.classList.add("display_none");
        isOpen = false;
    }
    else {
        menu.classList.remove("display_none");
        isOpen = true;
    }
}

function onResize() {
    if (window.innerWidth > 800 && isOpen) {
        menuOpen()
    }
}
window.addEventListener(`resize`, onResize);