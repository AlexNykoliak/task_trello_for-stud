import React from 'react';

const Card = ({ content, priority }) => {
  const priorityClass = {
    high: 'border-red-500',
    medium: 'border-yellow-500',
    low: 'border-green-500',
    default: 'border-blue-500',
  }[priority] || 'border-blue-500';

  return (
    <div className={`custom-card border-l-4 ${priorityClass}`}>
      <div className="custom-card-content">
        <p className="text-sm">{content}</p>
      </div>
      <div className="custom-card-footer">
        <small>Due Date: {'December 2023'}</small>
      </div>
    </div>
  );
};

export default Card;
