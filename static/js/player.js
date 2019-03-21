var initial = true
var played = []
var positions = []

function getNextMovie(){
    var params = {
        time_factor: time_factor,
        score_factor: score_factor,
    }
    if (initial) {
        params.origin_id = initial_mvid;
    }
    return axios
    .get('/api/player/', {params: params})
    .then( response => ( response.data.results[0].id ) )
    .then( mvid => ( app.mvid = mvid ) )
    .catch( error => function(){ console.log(error); app.broken = true; } )
}

function getSettings(){
    return axios
    .get('/api/settings')
    .then( response => ( app.settings = response.data ) )
    .then( function(){
        if (app.settings.time_factor == null || app.settings.score_factor == null){
            app.settings_show();
        }
    })
}

function moveMovie(e) {
    const player = document.getElementById('player');
    const origin = 'https://embed.nicovideo.jp';
    if (
        e.origin == origin
        && e.data.eventName == 'statusChange'
        && e.data.data.playerStatus == 4
    ){ //再生終了イベント
        app.playing = false
        getNextMovie();
    } else if (
        e.origin == origin
        && e.data.eventName == 'loadComplete'
    ){ //読み込み完了
        if(!initial){
        player.contentWindow.postMessage({
            sourceConnectorType: 1,
            eventName: 'play',
            }, origin
        )}
        initial = false;
    } else if (
        e.origin == origin
        && e.data.eventName == 'statusChange'
        && e.data.data.playerStatus == 3
    ){ //一時停止
        app.playing = false
    } else if (
        e.origin == origin
        && e.data.eventName == 'statusChange'
        && e.data.data.playerStatus == 2
    ){ //再生
        app.playing = true
    }
}

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

Vue.component('not-embeddable', {
    template: '<p class="my-auto">この動画はUTAKO TUNEでは対応していません。<br />考えられる理由: UTAKO TUNEで追跡していない、埋め込みが許可されていないなど</p>'
})

var r

r = new RegExp("[?&]origin_id=(([^&#]*)|&|#|$)").exec( location.search )
const initial_mvid = r ? (r[2] ? r[2] : null) : null

r = new RegExp("[?&]time_factor=(([^&#]*)|&|#|$)").exec( location.search )
const time_factor = r ? (r[2] ? r[2] : null) : null

r = new RegExp("[?&]score_factor=(([^&#]*)|&|#|$)").exec( location.search )
const score_factor = r ? (r[2] ? r[2] : null) : null

const app = new Vue({
    el: '#vuePlayer',
    data:{
        mvid: null,
        playing: false,
        broken: false,
        showModal: false,
    },
    created: function(){
        getSettings().then(getNextMovie())
    },
    computed:{
        playerComponent: function(){ return this.broken ? 'not-embeddable' : ( this.mvid ? 'niconico-player' : 'player-loading' ) },
        url: function(){ return 'https://embed.nicovideo.jp/watch/' + this.mvid + '?jsapi=1' },
        tweetUri: function(){
            return "https://twitter.com/intent/tweet?text="
            + encodeURI(
                'https://utako-tune.jp/ でこの曲を聞いています:\nhttp://nico.ms/'
                + this.mvid
                + '\nUTAKO TUNEでこの曲に似た曲を見る: https://utako-tune.jp/movie/'
                + this.mvid
                + '\nUTAKO TUNEでこの曲から連続再生: https://utako-tune.jp/player?origin_id='
                + this.mvid
            )
        }
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
        pause: function() {
            const player = document.getElementById('player');
            const origin = 'https://embed.nicovideo.jp';
            player.contentWindow.postMessage({
                sourceConnectorType: 1,
                eventName: 'pause',
                }, origin
            );
        },
        settings_show: () => ($('#settingsModal').modal('show')),
        settings_hide: () => ($('#settingsModal').modal('hide')),
    },
});

function submit_settings(){
    var search_factor = document.forms.settingsForm.elements.search_factor.value;
    var time_factor
    var score_factor

    if(search_factor[0] == '0'){
        time_factor = 5
    }else{
        time_factor = 0
    }

    if(search_factor[1] == '0'){
        score_factor = -5
    }else if(search_factor[1] == '2'){
        score_factor = 5
    }else{
        score_factor = 0
    }

    axios.patch('/api/settings/', {score_factor: score_factor, time_factor: time_factor})
    app.settings_hide()
}
