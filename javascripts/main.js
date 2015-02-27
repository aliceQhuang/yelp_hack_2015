var allUsers;

$(document).ready(function() {

    $.ajax({
        url: 'http://10.255.55.16:19000/everyone',
        success: function(result) {
            allUsers = JSON.parse(result);
            fillPokedexList(allUsers);
            fillPokedexContent(allUsers['aliceqh']);
        }
    });

    var setPortrait = function(id) {
        $('.image').css("background-image", ("url('images/people/" + id + ".jpg')"));
    }

    var _addHeaderTags = function() {
        headerTags = [
            '<h4 style="font-size:24px"><span id="header-id"></span></h4>',
            '<b>Region:&nbsp;&nbsp;&nbsp;</b>',
            '<span id="header-region"></span><br/>',
            '<b>Type:&nbsp;&nbsp;&nbsp;</b>',
            '<span id="header-type"></span><br/>',
            '<b>Ability:&nbsp;&nbsp;&nbsp;</b>',
            '<span id="header-ability"></span><br/>',
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

    var _addEvolutionTags = function(evolution_dict) {
        var evolutionTags = '';

        for (var id in evolution_dict) {
            if (id == 2) {
                evolutionTags = evolutionTags.concat(
                    '<div class="arrow-image-1"></div>'
                );
            }
            else if (id == 3) {
                evolutionTags = evolutionTags.concat(
                    '<div class="arrow-image-2"></div>'
                );
            }
            else if (id >= 4) {
                evolutionTags = evolutionTags.concat(
                    '<div class="arrow-image-3"></div>'
                );
            }
            evolutionTags = evolutionTags.concat(
                '<div class="evolution-image" id="' + evolution_dict[id] + '"></div>'
            );
        }

        $('.evolution-image-container').html(evolutionTags);
    }

    var _fillEvolutionTags = function(evolution_dict) {
        for (var id in evolution_dict) {
            $('#' + evolution_dict[id]).css("background-image", ("url('images/people/" + evolution_dict[id] + ".jpg')"));
        }
    }

    var generateEvolutionMarkup = function(evolution_dict) {
        _addEvolutionTags(evolution_dict);
        _fillEvolutionTags(evolution_dict);
    }

    var _addMoveTags = function(moves) {
        var moveMarkup = '';

        for (var move in moves) {
            if (moves.hasOwnProperty(move)) {
                moveMarkup = moveMarkup.concat(
                    '<b>Move ' + move + ':</b>&nbsp;&nbsp;&nbsp;&nbsp;',
                    '<span id="move-' + move + '"></span><br/>'
                );
            }
        }

        $('.details').html(moveMarkup);
    }

    var _fillMoveTags = function(moves) {
        for (var move in moves) {
            if (moves.hasOwnProperty(move)) {
                $('#move-' + move).text(moves[move]);
            }
        }
    }

    var generateMoveMarkup = function(moves) {
        _addMoveTags(moves);
        _fillMoveTags(moves);
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
            alice();
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
        generateEvolutionMarkup(user.evolution);
        generateMoveMarkup(user.move);
    }

    var blinkyblinky = function() {
        var el = $('blink h6')[0]
        if (el.style.visibility === 'visible') {
            el.style.visibility = 'hidden';
            el.style.color = getRandomColor();
            el.style.transform = 'none';
        } else {
            var a = Math.random() * 10 - 5;
            el.style.transform = 'rotate(' + a + 'deg) scale(1.25)';
            el.style.visibility = 'visible';
        }
    }

    var getRandomColor = function() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    setInterval(blinkyblinky, 250);
});
