var waitLoad = false
var played = []
var positions = []

function moveMovie(e) {
    const player = document.getElementById('player');
    const origin = 'https://embed.nicovideo.jp';
    if (
        e.origin == origin
        && e.data.eventName == 'statusChange'
        && e.data.data.playerStatus == 4
    ){
        app.mvid = generateMovie();
        waitLoad = true
    } else if (
        e.origin == origin
        && e.data.eventName == 'loadComplete'
        && waitLoad == true
    ){
        player.contentWindow.postMessage({
            sourceConnectorType: 1,
            eventName: 'play',
        }, origin)
        waitLoad == false
    }
}

function generateMovie() {
    var next_id = 'sm9'
    axios
        .get(
            '/api/vocalosphere/point/?origin=[' + getNextPosition().join(',') + ']')
        .then( response => ( next_id = response.data.results[0].id ) )
        .catch( error => ( console.log(error) ) )
    return next_id
}

const getNextPosition = function(){
    position = []
    for (i=0;i<8;i++) {
        position.push(Math.round(( Math.random() * 2 - 1  ) * 100) / 100);
    }
    return position;
}

window.addEventListener('message', moveMovie )

const app = new Vue({
    el: '#vuePlayer',
    data:{
        mvid: generateMovie(),
    },
    computed: {
        url: function() {
            return "https://embed.nicovideo.jp/watch/" + this.mvid + "?jsapi=1";
        }
    },
});
