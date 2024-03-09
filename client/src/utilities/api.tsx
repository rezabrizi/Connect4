
const API_BASE_URL = 'https://127.0.0.1:5000';


export const startNewGame = async (mode: string, difficulty: number) => {
    try 
    {
        const response = await fetch ('${API_BASE_URL}/new_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ players: mode === 'PVP' ? 2 : 1, difficulty}),
        }); 
        
        if (!response.ok){
            throw new Error ('Network response was not ok');
        }
        
        return response.json; 
    }
    catch (error)
    {
        console.error('Failed to start a new game', error);
        throw error;

    }
}