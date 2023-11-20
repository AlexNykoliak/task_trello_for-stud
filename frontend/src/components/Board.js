import React from 'react';
import Column from './Column';

const Board = () => {
  return (
    <div className="board flex">
      <Column title="To Do" />
      <Column title="In Progress" />
      <Column title="Done" />
    </div>
  );
};

export default Board;