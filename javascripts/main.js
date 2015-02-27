$(document).ready(function() {

    $('.pokemon').click(function (event) {
        var pokemon = $(event.target);
        var user = pokemon.data('user');
        $('.image').css("background-image", ("url('images/people/" + user + ".jpg')"));
        background: url('../img/me.jpg');
    });


});