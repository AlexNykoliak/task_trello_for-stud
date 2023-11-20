import React from 'react';
import Card from './Card';

const Column = ({ title }) => {
  return (
<div className="column bg-white rounded-lg shadow-md p-4 w-64">
  <h2 className="text-xl font-semibold mb-4">{title}</h2>
  <Card content="Finish project report" priority="high" />
  <Card content="Update website" priority="medium" />
  <Card content="Schedule meeting" priority="low" />
</div>
  );
};

export default Column;
