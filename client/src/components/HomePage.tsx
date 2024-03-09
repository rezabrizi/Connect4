import React, { useState } from 'react';

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

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>
                    Mode: 
                    <select value={localMode} onChange={e =>setLocalMode(e.target.value)}>
                        <option value="PvP"> Player vs Player</option>
                        <option value="PvB"> Player vs Bit</option>
                    </select>
                </label>
            </div>
            <button type="submit">Start Game</button>
        </form> 
    );
};

export default HomePage; 