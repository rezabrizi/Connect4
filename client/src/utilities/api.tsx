
const API_BASE_URL = 'http://127.0.0.1:5000';


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


export const makeMoveGame = async (game_id: string | null, column: number, is_bot_move: boolean) => {
    try
    {
        const response = await fetch (`${API_BASE_URL}/make_move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({game_id, column, is_bot_move}),
        });
        
        if (!response.ok){
            throw new Error ('Network response was not ok'); 
        }

        return response.json();
    }
    catch (error)
    {
        console.error('Failed to make a move', error);
        throw error
    }
}


