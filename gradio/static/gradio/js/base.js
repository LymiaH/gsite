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
      // Start playing this new one
      playing = document.getElementById(id);
      playing.play();
      if(btn) {
        playing_btn = btn;
        playing_btn.classList.add('playing');
      }
    }
  }
}
