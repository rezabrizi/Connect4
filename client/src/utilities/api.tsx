
const API_BASE_URL = 'https://146.190.170.64:8001';


export const startNewGame = async (mode: string, difficulty: number) => {
    try 
    {
        const response = await fetch (`${API_BASE_URL}/new_game`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ players: mode === 'PVP' ? 2 : 1, difficulty}),
        }); 
        
        if (!response.ok){
            throw new Error ('Network response was not ok');
        }
        
        return response.json(); 
    }
    catch (error)
    {
        console.error('Failed to start a new game', error);
        throw error;
    }
}


export const makePlayerMove = async (game_id: string, column: number) => {
    try {
        const response = await fetch(`${API_BASE_URL}/make_player_move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ game_id, column }),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Failed to make a player move', error);
        throw error;
    }
};

export const makeBotMove = async (game_id: string) => {
    try {
        const response = await fetch(`${API_BASE_URL}/make_bot_move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ game_id }),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Failed to make a bot move', error);
        throw error;
    }
};




