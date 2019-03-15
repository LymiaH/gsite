var gradio = function () {
  var playing = null;
  this.play = function(id) {
    // Pause currently playing
    if(playing) {
      playing.pause();
    }
    // If it is the same player
    if(playing && playing.id == id) {
      // Nothing is playing anymore
      playing = null;
    } else {
      // Start playing this new one
      playing = document.getElementById(id);
      playing.play();
    }
  }
}
