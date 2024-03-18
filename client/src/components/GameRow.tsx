import React from 'react'; 
import { Row } from 'src/components/interfaces/Row';
import { Column } from 'src/components/interfaces/Column';
import GameColumn from 'src/components/GameColumn';
import '../App.css';

interface Props {
    row: Row;
    playerMove: (columnIndex: number) => void;
    isLoading: boolean;
}

const GameRow: React.FC<Props> = ({ row, playerMove, isLoading }: Props): JSX.Element => {
    return (
        <tr>
            {row.columns.map(
                (column: Column, i: number):JSX.Element => (
                <GameColumn key ={i} column={column}  columnIndex={i} playerMove={playerMove} isLoading={isLoading}/>
                )
            )}
        </tr>
    )
}

export default GameRow; 