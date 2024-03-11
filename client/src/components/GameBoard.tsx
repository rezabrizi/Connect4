import React, { useState, useEffect } from 'react';
import  { c4Columns, c4Rows } from 'src/components/constants';
import { Board } from "src/components/interfaces/Board";
import { Row } from "src/components/interfaces/Row"; 
import GameRow from "src/components/GameRow"; 


import { startNewGame, makeMoveGame } from 'src/utilities/api'; 


interface GameBoardProps {
    mode: string;
    difficulty: number; 
}

const GameBoard: React.FC<GameBoardProps> = ({ mode, difficulty}) => {

    const initialBoard: Board = {
        rows: Array.from({ length: c4Rows }, (_, i) => ({
          columns: Array.from({ length: c4Columns }, (_, i) => ({ player: null })),
        })),
    };
    const [board, setBoard] = useState<Board>(initialBoard);
    const [currentPlayer, setCurrentPlayer] = useState<number>(0); 
    const [gameId, setGameId] = useState<string | null>(null); 
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const initializeGame = async () => {
            try {
                const gameData = await startNewGame(mode, difficulty);
                console.log(gameData.game_id);
                setGameId(gameData.game_id);
            } catch (error) {
                console.error("Failed to start new game:", error); 
            }
        };

        initializeGame();

    }, [mode, difficulty]);


    const updateBackEnd = async (columnIndex: number) => {
        try {
            console.log (gameId); 
            console.log(columnIndex);
            const moveData = await makeMoveGame(gameId, columnIndex, (currentPlayer === 1 && mode === 'PVB') ? true : false);
            
            return moveData.outcome; 
        } catch (error)
        {
            console.error("Failed to make a move", error);
        }
    };
    
    const updateBoard = async (columnIndex: number): Promise<void> => {
        setIsLoading(true);
        let boardCopy: Board = {
            rows: board.rows.map(row => ({
                columns: row.columns.map(column => ({
                    ...column
                }))
            }))
        };

        let isColumnFilled = false;
        for (let i = 5; i >= 0; i--) {
            if (boardCopy.rows[i].columns[columnIndex].player === null) {
                boardCopy.rows[i].columns[columnIndex].player = currentPlayer;
                isColumnFilled = false;
                break;
            }
        }

        if (!isColumnFilled) {
            // Update the board state before making the backend call
            setBoard({...boardCopy});

            // Now, make the backend call to update and check the game's state
            const outcome = await updateBackEnd(columnIndex);

            if (outcome === 0 || outcome === 1) {
                // Game is won by currentPlayer
                alert(`Game won by Player ${outcome}`);
                // Here you might want to reset the game or disable further moves
            } else if (outcome === -2) {
                // Game is tied
                alert('Game is tied');
                // Handle tie situation
            } else {
                // Game continues, toggle the current player
                setCurrentPlayer(currentPlayer === 0 ? 1 : 0);
            }
        }
        setIsLoading(false);
};

    

    return (
        <div> 
            <table>
                <thead></thead>
                <tbody>
                {board.rows.map(
                    (row:Row, i: number): JSX.Element => (
                    <GameRow key={i} row={row} updateBoard={updateBoard} isLoading={isLoading}/>
                    )
                    )}
                </tbody>
            </table>
        </div>
    );
};
export default GameBoard;