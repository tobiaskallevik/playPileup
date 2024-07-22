import React, { useState } from "react";
import { Card, Button } from "antd";
import { BorderOutlined } from "@ant-design/icons";
import '../styles/core.css';
const { Meta } = Card;

const GameCard = ({ title, image, description }) => {
  // State to manage hover
  const [isHovered, setIsHovered] = useState(false);

  return (
    <Card
      hoverable
      style={{ width: 260 }}
      className="game-card"
      cover={<img alt={title} src={image} />}
      
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Meta title={title} description={isHovered ? description : ''} />
    </Card>
  );
};

export default GameCard;