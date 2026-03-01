import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AuthProvider } from "react-oidc-context";
import './index.css'
import App from './App.tsx'
import { cognitoAuthConfig } from "./auth/cognitoConfig";
import { AlertProvider } from "./context/AlertContext";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider
      {...cognitoAuthConfig}
      onSigninCallback={() => {
        const cleanUrl = `${window.location.origin}${window.location.pathname}`;
        window.history.replaceState({}, document.title, cleanUrl);
      }}
    >
      <AlertProvider>
        <App />
      </AlertProvider>
    </AuthProvider>
  </StrictMode>,
)
