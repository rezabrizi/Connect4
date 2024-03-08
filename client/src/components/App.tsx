import React, {useState} from 'react';
import HomePage from './HomePage.tsx'
import GameBoard from './GameBoard.tsx'

interface StartGameParams {
    mode: string;
    difficulty: number;
}

function App() {
    const [gameStarted, setGameStarted] = useState<boolean>(false);
    const [mode, setMode] = useState<string>('PvP');
    const [difficulty, setDifficulty] = useState<number>(5);

    const onStartGame = ({mode, difficulty}: StartGameParams) => {
        setMode(mode); 
        setDifficulty (difficulty);
        setGameStarted(true);
    };

    return (
        <div className="App">
            {!gameStarted ? (
                <HomePage onStartGame={onStartGame} />
            ) : (
                <GameBoard mode={mode} difficulty={difficulty} />
            )}
        </div>
    );
}

export default App; 