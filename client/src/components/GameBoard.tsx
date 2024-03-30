import React, { useState, useEffect } from 'react';
import  { c4Columns, c4Rows } from 'src/components/constants';
import { Board } from "src/components/interfaces/Board";
import { Row } from "src/components/interfaces/Row"; 
import GameRow from "src/components/GameRow"; 


import { startNewGame, makePlayerMove, makeBotMove } from 'src/utilities/api'; 


interface GameBoardProps {
    mode: string;
    difficulty: number; 
    onEndGame:()=>void; 
  }
  

  const GameBoard: React.FC<GameBoardProps> = ({ mode, difficulty, onEndGame }) => {

    const initialBoard: Board = {
      rows: Array.from({ length: c4Rows }, () => ({
        columns: Array.from({ length: c4Columns }, () => ({ player: null })),
      })),
    };
  
    const [board, setBoard] = useState<Board>(initialBoard);
    const [currentPlayer, setCurrentPlayer] = useState<number>(0); 
    const [gameId, setGameId] = useState<string | null>(null); 
    const [isLoading, setIsLoading] = useState<boolean>(false);
  
    useEffect(() => {
      const initializeGame = async () => {
        setIsLoading(true);
        try {
          const gameData = await startNewGame(mode, difficulty);
          setGameId(gameData.game_id);
        } catch (error) {
          console.error("Failed to start new game:", error); 
        }
        setIsLoading(false);
      };
  
      initializeGame();
    }, [mode, difficulty]);

    const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));


    useEffect(() => {
      // Assuming `0` is the player and `1` is the bot in a PvB mode.
      const makeBotMoveIfNeeded = async () => {
        if (mode === 'PVB' && currentPlayer === 1 && !isLoading) {
          await botMove();
        }
      };
  
      makeBotMoveIfNeeded();
    }, [currentPlayer, mode, isLoading])
    
  
    const playerMove = async (columnIndex: number) => {
      if (!gameId || isLoading) return;
      setIsLoading(true);
  
      try {
        const moveData = await makePlayerMove(gameId, columnIndex);
        if (moveData.error) {
          alert(moveData.error);
          setIsLoading(false);
          return;
        }
        console.log(`Player Move: ${currentPlayer}\n${moveData.row} \n${moveData.column}\n${moveData.outcome}`);
        await updateBoard(moveData.row, columnIndex);
        console.log(`Turn ${currentPlayer}`);
  
        await delay(200);

        if (moveData.outcome === 0 || moveData.outcome === 1) {
          alert(`Player ${moveData.outcome + 1} wins!`);
          resetGame();
          return;
        } else if (moveData.outcome === -2) {
          alert("It's a tie!");
          resetGame();
          return;
        } 
      } catch (error) {
        console.error("Failed to make a player move", error);
      } finally {
        setIsLoading(false);
      }
    };
  
    const botMove = async () => {
      if (!gameId) return;
      try {
        setIsLoading(true);
        const moveData = await makeBotMove(gameId);
        if (moveData.error) {
          alert(moveData.error);
          return;
        }
        console.log(`Bot Move: ${currentPlayer} \n${moveData.row} \n${moveData.column}\n${moveData.outcome}`);
  
        await updateBoard(moveData.row, moveData.column);
        
        await delay(200);

        if (moveData.outcome === 0 || moveData.outcome === 1) {
          alert(`Player ${moveData.outcome + 1} wins!`);
          resetGame();
        } else if (moveData.outcome === -2) {
          alert("It's a tie!");
          resetGame();
        }
      } catch (error) {
        console.error("Failed to make a bot move", error);
      } finally {
        setIsLoading(false);
      }
    };
  
    const updateBoard = async (rowIndex: number, columnIndex: number) => {
      let newBoard = { ...board };
      newBoard.rows[rowIndex].columns[columnIndex].player = currentPlayer;
      setBoard(newBoard);
      setCurrentPlayer((currentPlayer + 1) % 2);
    };
  
    const resetGame = () => {
      setBoard(initialBoard);
      setCurrentPlayer(0);
      setIsLoading(false);
      onEndGame(); 
    };
  
    

    return (
        <div> 
            <table>
                <thead></thead>
                <tbody>
                {board.rows.map(
                    (row:Row, i: number): JSX.Element => (
                    <GameRow key={i} row={row} playerMove={playerMove} isLoading={isLoading}/>
                    )
                    )}
                </tbody>
            </table>
        </div>
    );
};
export default GameBoard;