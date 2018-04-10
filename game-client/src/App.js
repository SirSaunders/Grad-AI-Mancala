import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'
class App extends Component {

  constructor(props){
    super(props)
    this.state = {
    "board": {
        "space": [{
            "type": "mancala",
            "marbles": 0,
            "space_id": 0,
            "player": 1
        },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 1,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 2,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 3,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 4,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 5,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 6,
                "player": 0
            },
            {
                "type": "mancala",
                "marbles": 0,
                "space_id": 7,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 8,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 9,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 10,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 11,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 12,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 13,
                "player": 1
            }
        ]
    }
}

    this.getButtons = this.getButtons.bind(this);
        this.moveSelected = this.moveSelected.bind(this);

  }
    aiMove(){
      var json = { "board": this.state.board}

                var data = JSON.stringify(json);

                  axios({
                          baseURL: 'http://127.0.0.1:8000/get_move',
                          timeout: 30000,
                          headers: {'Content-Type': 'application/json'},
                       data: data,
                        method: 'post'
                        })
                      .then(function (response) {
                        console.log(response);
                        var board = this.state.board

                          board.space = response.data.board.space
                          console.log(board)
                        this.setState({board:board})
                          if(board.ai_goes_again){
                            this.aiMove()
                          }
                      }.bind(this))
                      .catch(function (error) {
                        console.log(error);
                      }.bind(this));
    }
    moveSelected(move){
        var json = {"move":parseInt(move), "board": this.state.board}

                var data = JSON.stringify(json);

                  axios({
                          baseURL: 'http://127.0.0.1:8000/update_board',
                          timeout: 30000,
                          headers: {'Content-Type': 'application/json'},
                       data: data,
                        method: 'post'
                        })
                      .then(function (response) {
                        console.log(response);
                        var board = this.state.board
                          board.space = response.data
                          console.log(board)
                        this.setState({board:board})
                          this.aiMove()
                      }.bind(this))
                      .catch(function (error) {
                        console.log(error);
                      }.bind(this));


    }
   getButtons(rangestart,rangeEnd) {
        var returnBtns = [];
        for (var i = rangestart; i <= rangeEnd; i++){
            returnBtns.push( <button id = {i} key={i} onClick={()=>this.moveSelected(4)}>{this.state.board.space[i].marbles}</button>)
        }
        return returnBtns;

    }
  render() {

    return (
      <div className="App" style ={{'width':'400px'}}>
              <h1 style = {{"float":"left"}}> {this.state.board.space[0].marbles}</h1>
          <div>
                {this.getButtons(1,6)}
          </div>

      <div>
                {this.getButtons(8,13)}

        </div>
              <h1 style = {{"float":"right"}}> {this.state.board.space[7].marbles}</h1>


      </div>

    );
  }
}

export default App;
