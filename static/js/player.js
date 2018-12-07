var initial = true
var played = []
var positions = []

function getNextMovie(){
    axios
    .get(initial && initial_mvid
        ? '/api/player?origin_id='+initial_mvid
        : '/api/player')
    .then( response => ( response.data.results[0].id ) )
    .then( mvid => ( app.mvid = mvid ) )
    .catch( error => ( console.log(error) ) )
}

function moveMovie(e) {
    const player = document.getElementById('player');
    const origin = 'https://embed.nicovideo.jp';
    if (
        e.origin == origin
        && e.data.eventName == 'statusChange'
        && e.data.data.playerStatus == 4
    ){
        getNextMovie();
    } else if (
        e.origin == origin
        && e.data.eventName == 'loadComplete'
    ){
        if(!initial){
        player.contentWindow.postMessage({
            sourceConnectorType: 1,
            eventName: 'play',
            }, origin
        )}
        initial = false;
}}

window.addEventListener('message', moveMovie )

Vue.component('player-loading', {
    template: '<div id="floatingCirclesG">\n'
            + '<div class="f_circleG" id="frotateG_01"></div>\n'
            + '<div class="f_circleG" id="frotateG_02"></div>\n'
            + '<div class="f_circleG" id="frotateG_03"></div>\n'
            + '<div class="f_circleG" id="frotateG_04"></div>\n'
            + '<div class="f_circleG" id="frotateG_05"></div>\n'
            + '<div class="f_circleG" id="frotateG_06"></div>\n'
            + '<div class="f_circleG" id="frotateG_07"></div>\n'
            + '<div class="f_circleG" id="frotateG_08"></div>\n'
            + '</div>'
})

Vue.component('niconico-player', {
    template: '<iframe class="embed-responsive-item" frameborder="no" scrolling="no" allow="fullscreen" id="player"></iframe>'
})

const r = new RegExp("[?&]origin_id=(([^&#]*)|&|#|$)").exec( location.search )[2]
const initial_mvid = r ? r : null

const app = new Vue({
    el: '#vuePlayer',
    data:{
        mvid: null,
    },
    created: function(){
        getNextMovie();
    },
    computed:{
        playerComponent: function(){ return this.mvid ? 'niconico-player' : 'player-loading' },
        url: function(){ return 'https://embed.nicovideo.jp/watch/' + this.mvid + '?jsapi=1' },
    },
    methods:{
        next: () => (getNextMovie()),
        play: function() {
            const player = document.getElementById('player');
            const origin = 'https://embed.nicovideo.jp';
            player.contentWindow.postMessage({
                sourceConnectorType: 1,
                eventName: 'play',
                }, origin
            );
        },
    },
});
