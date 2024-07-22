import React from 'react';
import {Typography} from "antd";
import MainLayout from '../components/MainLayout.jsx';
import GameCard from '../components/GameCard.jsx';
import games from '../../../assets/games.json'
import '../styles/core.css';

export default function Home() {

  games.forEach(game => {
    console.log(game.name);
  });

  return (
    <MainLayout>
      <div className='gameContainer'>
        {games.map((game, index) => (
          <GameCard
            key={index}
            image={game.cover_url_high} 
            title={game.name}
            description={game.description} 
          />
        ))}
      </div>
    </MainLayout>
  );
}

