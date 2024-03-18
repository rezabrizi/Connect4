import React from 'react'; 
import { Column } from 'src/components/interfaces/Column';


interface Props {
    columnIndex: number;
    column: Column; 
    playerMove: (columnIndex: number) => void;
    isLoading: boolean;
}


const GameColumn: React.FC<Props> = ({columnIndex, column, playerMove, isLoading}: Props): JSX.Element => {
    
    let tileStatus = "open";
    if (column.player === 0){
        tileStatus = "player0";
    }
    else if (column.player === 1){
        tileStatus = "player1";
    }
    return (
        <td> 
            <div className='tile' onClick= {() => !isLoading && playerMove(columnIndex)}>
                <div className={[tileStatus, "circle"].join(" ")}></div>
            </div>
        </td>
    )
}

export default GameColumn;