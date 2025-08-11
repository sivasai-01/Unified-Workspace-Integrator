import { IntegrationForm } from './integration-form';
import { Box, Typography } from '@mui/material';

function App() {
  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="flex-start"
      minHeight="100vh"
      sx={{
        background: 'linear-gradient(90deg, #e3ffe8 0%, #f9f9f9 100%)',
        py: 4,
      }}
    >
      <Typography
        variant="h3"
        align="center"
        sx={{
          fontWeight: 700,
          color: '#1976d2',
          mb: 4,
          letterSpacing: 2,
          textShadow: '0 2px 8px rgba(25, 118, 210, 0.1)',
        }}
      >
        Unified Workspace Integrator
      </Typography>
      <IntegrationForm />
    </Box>
  );
}

export default App;
