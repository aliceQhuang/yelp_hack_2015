var allUsers;

$(document).ready(function() {

    $.ajax({
        url: 'http://10.255.55.16:19000/everyone',
        success: function(result) {
            allUsers = JSON.parse(result);
            fillPokedexList(allUsers);
            fillPokedexContent(allUsers['jeremy']);
        }
    });

    var setPortrait = function(id) {
        $('.image').css("background-image", ("url('images/people/" + id + ".jpg')"));
    }

    var generateHeaderMarkup = function(id, region, type, ability) {
        return [
            '<h4 style="font-size:24px">',
                id,
            '</h4>',
            '<p>',
                '<b>Region:&nbsp;&nbsp;</b>',
                region,
                'F<br/>',
                '<b>Type:&nbsp;&nbsp;</b>',
                type,
                '<br/>',
                '<b>Ability:&nbsp;&nbsp;</b>',
                ability,
                '<br/>',
            '</p>'
        ].join('');
    }

    var fillPokedexList = function(allUsers) {
        var listMarkup = '<h3>Pokemon List</h3>';

        for (var user in allUsers) {
            if (allUsers.hasOwnProperty(user)) {
                userObj = allUsers[user]
                listMarkup = listMarkup.concat([
                    '<a class="pokemon" href="javascript:;" data-user="' + userObj.id + '">',
                        userObj.id,
                    '</a>',
                    '<br />'
                ].join(''));

            }
        }

        $('.list-container').html(listMarkup);

        $('.pokemon').click(function (event) {
            var pokemon = $(event.target);
            var user = pokemon.data('user');
            fillPokedexContent(allUsers[user]);
        });
    }

    var fillPokedexContent = function(user) {
        var headerMarkup = generateHeaderMarkup(
            user.id,
            user.region,
            user.type,
            user.ability
        )

        $('.headers').html(headerMarkup);
        setPortrait(user.id);
    }

});

