import React, { useState, useEffect } from 'react';
import  { c4Columns, c4Rows } from 'src/components/constants';
import { Board } from "src/components/interfaces/Board";
import { Row } from "src/components/interfaces/Row"; 
import GameRow from "src/components/GameColumn"; 

import { startNewGame } from 'src/utilities/api'; 


interface GameBoardProps {
    mode: string;
    difficulty: number; 
}

const GameBoard: React.FC<GameBoardProps> = ({ mode, difficulty}) => {

    const initialBoard:Board= {
        rows: Array.from({length: c4Columns}, (_, i) => ({
            columns: Array.from({length: c4Columns}, (_, i) => ({
                player: null
            })) 
        }))
    };

    const [currentPlayer, setCurrentPlayer] = useState<number>(1); 
    const [board, setBoard] = useState<Board>(initialBoard);

    const handlePlayerMove = () => {
        // call the backend api 

        setCurrentPlayer(currentPlayer === 1 ? 2: 1); 
    }


    return (
        <div> 
            <table>
                <tbody>
                {board.rows.map((row:Row, i: number): JSX.Element => (<GameRow key={i} row={row}/>))}
                </tbody>
            </table>
        </div>
    )
    
} 
export default GameBoard;