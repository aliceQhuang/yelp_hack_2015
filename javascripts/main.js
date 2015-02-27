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

    var _addHeaderTags = function() {
        headerTags = [
            '<h4 style="font-size:24px"><span id="header-id"></span></h4>',
            '<p>',
                '<b>Region:&nbsp;&nbsp;</b>',
                '<span id="header-region"></span><br/>',
                '<b>Type:&nbsp;&nbsp;</b>',
                '<span id="header-type"></span><br/>',
                '<b>Ability:&nbsp;&nbsp;</b>',
                '<span id="header-ability"></span><br/>',
            '</p>'
        ].join('');
        $('.headers').html(headerTags);
    }

    var _fillHeaderTags = function(id, region, type, ability) {
        $('#header-id').text(id);
        $('#header-region').text(region);
        $('#header-type').text(type);
        $('#header-ability').text(ability);
    }

    var generateHeaderMarkup = function(id, region, type, ability) {
        _addHeaderTags();
        _fillHeaderTags(id, region, type, ability);
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
        generateHeaderMarkup(
            user.id,
            user.region,
            user.type,
            user.ability
        )
        setPortrait(user.id);
    }
});
