/**
 # @Authors: Johnathan Saunders && Jatin Bhakta
# @Date: 4/18/18
# @Class: Graduate AI Class
 */

import React, { Component } from 'react';
import './App.css';
import axios from 'axios'
class App extends Component {

    constructor(props) {
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
            },
            "isAiTurn": false,
            "winner": null
        }
        //this.getButtons = this.getButtons.bind(this); //under development
        this.moveSelected = this.moveSelected.bind(this);

    }
    /**
     * sends the current board state to server to get AI's move
     * Then updates the board state
     * */
    aiMove() {
        if(this.state.winner == null) {
            this.setState({"isAiTurn": true})
            var json = {"board": this.state.board}

            var data = JSON.stringify(json);

            axios({
                baseURL: 'http://127.0.0.1:8000/get_move',
                timeout: 60000,
                headers: {'Content-Type': 'application/json'},
                data: data,
                method: 'post'
            })
                .then(function (response) {
                    console.log(response);
                    var board = this.state.board
                    board.space = response.data.board.space
                    console.log(board) // prints returned board state
                    this.setState({board: board, winner: response.data.winner})
                    if (response.data.go_again) { // call endpoint again if AI can go again
                        this.aiMove()
                    } else {
                        this.setState({"isAiTurn": false})
                    }
                }.bind(this))
                .catch(function (error) {
                    console.log(error);
                }.bind(this));
        }
    }
    /**
     * sends move user selected to end point along with current board's state
     * then updates the board state on response
     * */
    moveSelected(move) {
        if (!this.state.isAiTurn && this.state.winner == null) {

            console.log(move)
            var json = { "move": parseInt(move), "board": this.state.board }

            var data = JSON.stringify(json);

            axios({
                baseURL: 'http://127.0.0.1:8000/update_board',
                timeout: 30000,
                headers: { 'Content-Type': 'application/json' },
                data: data,
                method: 'post'
            })
                .then(function (response) {
                    console.log(response);
                    var board = this.state.board
                    board.space = response.data.board.space
                    console.log(board)
                    this.setState({ board: board, winner:response.data.winner })
                    if (!response.data.go_again) { // let ai go if player is not allowed to go again
                        this.aiMove()
                    }
                }.bind(this))
                .catch(function (error) {
                    console.log(error);
                }.bind(this));
        }

    }
/*
the below commented out code is still under developpment in an attempt to replace the button's code duplication
*/
    // getButtons(rangestart, rangeEnd) {
    //     var returnBtns = [];
    //     for (var i = rangestart; i <= rangeEnd; i++) {
    //         returnBtns.push(<button id={i} key={i} onClick={() => this.moveSelected(10)}>{this.state.board.space[i].marbles}</button>)
    //     }
    //     return returnBtns;
    //
    // }

    componentDidMount() {

    }

    render() {

        return (

            <div>
                <h1 style={{ "text-align": "center", marginTop: "15vh"}}> AI Mancala </h1>

            <div className="App" style={{
                    'width': '400px',
                    margin: "auto",
                    width: "50%",
                    border: "3px solid green",
                    padding: "10px",
                    backgroundColor: "#e3eff2",
                    marginTop: "10vh"
                }}>
                    {/* <img src={logo} className="App-logo" alt="logo" /> */}
                    <h1 style={{ "float": "left" }}> AI:&nbsp;</h1>
                    <h1 style={{ "float": "left" }}> {this.state.board.space[7].marbles}</h1>

                    <h1 style={{ "float": "right" }}> {this.state.board.space[0].marbles}</h1>
                    <h1 style={{ "float": "right" }}> You:&nbsp; </h1>

                    <div style={{ 'paddingTop': '20px' }}>
                        <button>{this.state.board.space[6].marbles}</button>
                        <button>{this.state.board.space[5].marbles}</button>
                        <button>{this.state.board.space[4].marbles}</button>
                        <button >{this.state.board.space[3].marbles}</button>
                        <button >{this.state.board.space[2].marbles}</button>
                        <button >{this.state.board.space[1].marbles}</button>
                    </div>

                    <div>
                        <button onClick={() => this.moveSelected(8)}>{this.state.board.space[8].marbles}</button>
                        <button onClick={() => this.moveSelected(9)}>{this.state.board.space[9].marbles}</button>
                        <button onClick={() => this.moveSelected(10)}>{this.state.board.space[10].marbles}</button>
                        <button onClick={() => this.moveSelected(11)}>{this.state.board.space[11].marbles}</button>
                        <button onClick={() => this.moveSelected(12)}>{this.state.board.space[12].marbles}</button>
                        <button onClick={() => this.moveSelected(13)}>{this.state.board.space[13].marbles}</button>
                    </div>

                    <div>  {(this.state.isAiTurn && this.state.winner == null) ?
                        <img width={100} src="https://media.giphy.com/media/xTk9ZvMnbIiIew7IpW/giphy.gif" />
                        :
                        (this.state.winner == null)?
                        <h1>Your Turn</h1>
                            :
                            <h1> {this.state.winner} is the winner</h1>

                    }

                    </div>

                </div>
            </div>

        );
    }
}

export default App;
