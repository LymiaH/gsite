var gradio = function () {
  var playing = null;
  var playing_btn = null;
  this.play = function(id, btn=null) {
    // Pause currently playing
    if(playing) {
      playing.pause();
      if(playing_btn) {
        playing_btn.classList.remove('playing');
      }
    }
    // If it is the same player
    if(playing && playing.id == id) {
      // Nothing is playing anymore
      playing = null;
      playing_btn = null;
    } else {
      // Get player
      playing = document.getElementById(id);
      // If it is a video element, check if there is a stream_src and bind it
      if(playing.nodeName == "VIDEO") {
        var stream_src = playing.getAttribute("stream_src")
        if(stream_src) {
          playing.removeAttribute("stream_src")
          // https://github.com/video-dev/hls.js#getting-started
          if(Hls.isSupported()) {
            var hls = new Hls();
            hls.loadSource(stream_src);
            hls.attachMedia(playing);
          } else if (playing.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = stream_src;
          }
        }
      }
      // Start playing this new one
      playing.play();
      if(btn) {
        playing_btn = btn;
        playing_btn.classList.add('playing');
      }
    }
  }
}
