import React, { useState } from 'react';
import { TextField, Button, Box, Paper } from '@mui/material';

const MusicForm = ({ onSubmit }) => {
  const [mood, setMood] = useState('');
  const [genre, setGenre] = useState('');
  const [lyrics, setLyrics] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({ mood, genre, lyrics });
  };

  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="心情" value={mood} onChange={(e) => setMood(e.target.value)} required />
        <TextField label="曲風" value={genre} onChange={(e) => setGenre(e.target.value)} required />
        <TextField label="歌詞" value={lyrics} onChange={(e) => setLyrics(e.target.value)} required multiline rows={4} />
        <Button type="submit" variant="contained">生成音樂</Button>
      </Box>
    </Paper>
  );
};

export default MusicForm;
