import React, {useState} from 'react';
import HomePage from './components/HomePage'
import GameBoard from './components/GameBoard'
import './App.css';


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

    const onEndGame = () => {
        setGameStarted(false); 
    }

    return (
        <div className="App">
            {!gameStarted ? (
                <HomePage onStartGame={onStartGame} />
            ) : (
                <GameBoard mode={mode} difficulty={difficulty} onEndGame={onEndGame}/>
            )}
        </div>
    );
}

export default App; 