class BoggleGame {
  
    constructor(boardId, secs = 60) {
    // setting the timer and displaying it
      this.secs = secs; 
      this.showTimer();
  
    //   setting the intial score and board
      this.score = 0;
      this.words = new Set();
      this.board = $("#" + boardId);
  
      this.timer = setInterval(this.tick.bind(this), 1000);
  
      $(".word-form", this.board).on("submit", this.handleSubmit.bind(this));
    }
  
    // function to display the words that have been quessed
  
    showWord(word) {
      $(".words", this.board).append($("<li>", { text: word }));
    }
  
    // function that shows the score on the page
  
    showScore() {
      $(".score", this.board).text(this.score);
    }
  
    // function that displays user facing messages on the page 
  
    showMessage(msg, cls) {
      $(".msg", this.board)
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }
  
    // handle submission of word while checking its validity 
    // also handles calling necessary functions on word submission
  
    async handleSubmit(evt) {
      evt.preventDefault();
      const $word = $(".word", this.board);
  
      let word = $word.val();
      if (!word) return;
  
      if (this.words.has(word)) {
        this.showMessage(`Already found ${word}`, "err");
        return;
      }
  
      // check the server
      const resp = await axios.get("/check-word", { params: { word: word }});
      if (resp.data.result === "not-word") {
        this.showMessage(`${word} is not a valid English word`, "err");
      } else if (resp.data.result === "not-on-board") {
        this.showMessage(`${word} is not a valid word on this board`, "err");
      } else {
        this.showWord(word);
        this.score += word.length;
        this.showScore();
        this.words.add(word);
        this.showMessage(`Added: ${word}`, "ok");
      }
  
      $word.val("").focus();
    }
  
    
    // function that updates the timer on the page
    showTimer() {
      $(".timer", this.board).text(this.secs);
    }
  
    // handle the passing seconds
    async tick() {
      this.secs -= 1;
      this.showTimer();
  
      if (this.secs === 0) {
        clearInterval(this.timer);
        await this.scoreGame();
      }
    }
  
    // handles the end of the game
    async scoreGame() {
      $(".word-form", this.board).hide();
      const resp = await axios.post("/post-score", { score: this.score });
      if (resp.data.brokeRecord) {
        this.showMessage(`New record: ${this.score}`, "ok");
      } else {
        this.showMessage(`Final score: ${this.score}`, "ok");
      }
    }
  }