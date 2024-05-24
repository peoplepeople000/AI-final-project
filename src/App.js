import React, { useState } from 'react';
import { Container, Typography, Box } from '@mui/material';
import MusicForm from './MusicForm';
import MusicPlayer from './MusicPlayer';

const App = () => {
  const [musicUrl, setMusicUrl] = useState('');

  const handleGenerateMusic = async (data) => {
    const response = await fetch('http://localhost:5000/generate-music', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    setMusicUrl(result.musicUrl);
  };

  return (
    <Box
      sx={{
        backgroundImage: 'url(https://source.unsplash.com/random)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        p: 2,
      }}
    >
      <Container
        sx={{
          bgcolor: 'rgba(255, 255, 255, 0.8)',
          borderRadius: 2,
          boxShadow: 3,
          p: 4,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom align="center">音樂生成器</Typography>
        <MusicForm onSubmit={handleGenerateMusic} />
        <MusicPlayer musicUrl={musicUrl} />
      </Container>
    </Box>
  );
};

export default App;
