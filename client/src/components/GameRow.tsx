import React from 'react'; 
import { Row } from 'src/components/interfaces/Row';
import { Column } from 'src/components/interfaces/Column';
import GameColumn from 'src/components/GameColumn';
import '../App.css';

interface Props {
    row: Row;
    updateBoard: (columnIndex: number) => void;
    isLoading: boolean;
}

const GameRow: React.FC<Props> = ({ row, updateBoard, isLoading }: Props): JSX.Element => {
    return (
        <tr>
            {row.columns.map(
                (column: Column, i: number):JSX.Element => (
                <GameColumn key ={i} column={column}  columnIndex={i} updateBoard={updateBoard} isLoading={isLoading}/>
                )
            )}
        </tr>
    )
}

export default GameRow; 