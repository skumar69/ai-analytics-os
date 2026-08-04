import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider, CssBaseline, createTheme } from '@mui/material'
import { AuthProvider } from './context/AuthContext.jsx'
import './index.css'
import App from './App.jsx'

// Inline minimal theme to avoid module evaluation crash
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary:   { main: '#1976d2' },
    secondary: { main: '#7c3aed' },
    success:   { main: '#2e7d32' },
    warning:   { main: '#ed6c02' },
    error:     { main: '#d32f2f' },
    background: { default: '#0f172a', paper: '#1a2744' },
    text:       { primary: '#f1f5f9', secondary: '#94a3b8' },
  },
  typography: { fontFamily: '"Inter", "Segoe UI", Arial, sans-serif' },
  shape: { borderRadius: 12 },
  components: {
    MuiButton:  { styleOverrides: { root: { textTransform: 'none', fontWeight: 600 } } },
    MuiChip:    { styleOverrides: { root: { fontWeight: 600 } } },
  },
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>,
)
