import React, {useEffect, useState } from 'react'; 


interface GameBoardProps { 
    mode: string; 
    difficulty: number
}

const GameBoard: React.FC<GameBoardProps> = ({mode, difficulty}) => {

    const [board, setBoard] = useState([]);


    const intializeGame = async () => {

    };

    const makeMove = async (column, isBotMove = false) => {

    };

    const updateBoard = async() => {


    };



    return (
        <div>

        </div>
    );
};
export default GameBoard; 