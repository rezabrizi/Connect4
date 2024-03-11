import React, { useState } from 'react';
import '../App.css';

interface HomePageProps {
    onStartGame : (params: {mode: string; difficulty: number; }) => void; 
}

const HomePage: React.FC<HomePageProps> = ({ onStartGame }) => {
    const [localMode, setLocalMode] = React.useState<string>('PvP'); 
    const [localDifficulty, setLocalDifficulty] = React.useState<number>(5);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        onStartGame({mode: localMode, difficulty: localDifficulty}); 
    }

    const handleDifficultyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = parseInt(e.target.value);
        if (!isNaN(value) && value >= 1 && value <= 10) {
            setLocalDifficulty(value);
        }
    };

    return (
        <div className = "App">
            <h1>Connect 4</h1>
            <form className="homepage-form" onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="modeSelect">Mode:</label>
                    <select id="modeSelect" value={localMode} onChange={e =>setLocalMode(e.target.value)}>
                        <option value="PVP"> Player vs Player</option>
                        <option value="PVB"> Player vs Bot</option>
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="difficultySelect">Difficulty (1-10):</label>
                    <input
                    type="range"
                    id="difficultyInput"
                    min={1}
                    max={10}
                    value={localDifficulty}
                    onChange={handleDifficultyChange}
                    />
                    <span>{localDifficulty}</span>
                </div>
                <button type="submit">Start Game</button>
            </form> 
        </div>
    );
};

export default HomePage; 