import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const MusicPlayer = ({ musicUrl }) => {
  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">音樂播放器</Typography>
        {musicUrl ? (
          <audio controls style={{ width: '100%' }}>
            <source src={musicUrl} type="audio/mpeg" />
            您的瀏覽器不支持音樂播放。
          </audio>
        ) : (
          <Typography variant="body2" color="text.secondary">請生成音樂後再播放。</Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default MusicPlayer;
