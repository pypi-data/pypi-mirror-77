/**
 * dynamic field - JavaScript
 *
 * @link    https://joseflorez.co
 * @license For open source use: MIT
 * @author  Jose Florez https://joseflorez.co
 * @version 1.0.0
 *
 * See usage examples at https://joseflorez.co/
 */

let scroll = document.body.getBoundingClientRect().top;
let header = document.getElementById('headerUI');
let opacity = document.getElementById('opacityDisplay').classList;
let toggleAction = document.getElementById('toggleAction');
let isScrolling = 0;

if (header) header_fixed ? header.classList.add('active') : header.classList.add('top');

window.addEventListener('scroll', function (event) {
    isScrolling = (document.body.getBoundingClientRect()).top;
    if (header_fixed) {
        if (isScrolling > scroll && isScrolling < -100) {
            header.classList.add('active')
        } else if (isScrolling < -100) {
            header.classList.remove('active');
            toggleAction.innerHTML = '<i class="fas fa-bars"></i>';
        } else {
            header.classList.add('active')
        }
    } else {
        if (isScrolling > scroll && isScrolling < -100) {
            header.classList.add('active')
            header.classList.remove('top');
        } else if (isScrolling < -100) {
            header.classList.remove('top');
            opacity.remove('active');
            toggleAction.innerHTML = '<i class="fas fa-bars"></i>';
        } else {
            header.classList.remove('active')
            header.classList.add('top')
            if (header.classList.contains('activeTop')) {
                opacity.add('active');
                toggleAction.innerHTML = '<i class="fas fa-times"></i>';
            }
        }
    }
    scroll = isScrolling;

}, false);

// toggle
document.getElementById("opacityDisplay").addEventListener("click", function () {
    navAction();
});
document.getElementById("toggleAction").addEventListener("click", function () {
    navAction();
});

function navAction() {
    let element = document.getElementById("navMenu").classList;
    if(header_fixed) {
        element.toggle('active');
        if (element.contains('active')) {
            toggleAction.innerHTML = '<i class="fas fa-times"></i>';
            opacity.add('active');
        } else {
            toggleAction.innerHTML = '<i class="fas fa-bars"></i>';
            opacity.remove('active');
        }
    } else {
        if (isScrolling > -100) {
            if (header.classList.contains('activeTop')) {
                header.classList.remove('activeTop');
                toggleAction.innerHTML = '<i class="fas fa-bars"></i>';
                opacity.remove('active');
            } else {
                header.classList.add('activeTop');
                toggleAction.innerHTML = '<i class="fas fa-times"></i>';
                opacity.add('active');
            }
        } else {
            if (element.contains('active')) {
                element.remove('active');
            } else {
                element.add('active')
            }
        }
    }
}

// sub menu

// Initialize all event handlers on page load
document.addEventListener('DOMContentLoaded', function () {
    let list_sub = document.querySelectorAll('li.dropdown a');
    for (let i = 0; i < list_sub.length; i++) {
        eventSubMenu(list_sub[i]);
    }
});

function eventSubMenu(item) {
    item.addEventListener('click', function (event) {
        if(!event.target.classList.contains('sub_')) {
            event.target.removeAttribute("href");
            showHiddenSubMenu(event.target);
        }
    })
}

function showHiddenSubMenu(item) {
    let ul = item.parentNode.querySelector('ul');
    if (ul) {
        ul.classList.toggle('active');
    }
}