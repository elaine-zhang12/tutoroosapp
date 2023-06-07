function hovered_home(){
    anime({
        targets: '.home_icon',
        strokeDashoffset: [anime.setDashoffset, 0],
        easing: 'linear',
        duration: 1000,
        delay: function(el, i) { return i * 0050 },
        loop: false
    });
   
}
function hovered_bell(){
    anime({
        targets: '.bell_icon',
        strokeDashoffset: [anime.setDashoffset, 0],
        easing: 'linear',
        duration: 1000,
        delay: function(el, i) { return i * 0050 },
        loop: false
    });
}

function hovered_acc(){
    anime({
        targets: '.account_icon',
        strokeDashoffset: [anime.setDashoffset, 0],
        easing: 'linear',
        duration: 1000,
        delay: function(el, i) { return i * 0050 },
        loop: false
    });
}
