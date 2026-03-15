import { useAuth } from "react-oidc-context";
import { useEffect, useRef } from "react";
import { isExpectedSignedOutAuthError } from "./auth/authError";
import { useAlert } from "./context/AlertContext";
import Container from './components/Container';

function App() {
  const auth = useAuth();
  const { setAlert } = useAlert();
  const hasAttemptedSilentSignIn = useRef(false);
  const { activeNavigator, error, isAuthenticated, isLoading, signinSilent } = auth;

  useEffect(() => {
    const message = error?.message;
    if (!message) {
      setAlert(null);
      return;
    }

    if (isExpectedSignedOutAuthError(message)) {
      setAlert(null);
      return;
    }

    if (error) {
      setAlert({
        kind: "error",
        message: `Sign-in failed: ${message}`,
      });
      return;
    }

    setAlert(null);
  }, [error, setAlert]);

  useEffect(() => {
    if (hasAttemptedSilentSignIn.current) {
      return;
    }

    if (isLoading || activeNavigator) {
      return;
    }

    if (error || isAuthenticated) {
      hasAttemptedSilentSignIn.current = true;
      return;
    }

    hasAttemptedSilentSignIn.current = true;
    void signinSilent().catch(() => {
      // Expected when there is no existing Cognito session; UI stays signed-out.
    });
  }, [activeNavigator, error, isAuthenticated, isLoading, signinSilent]);

return (
      <div
        className="app"
        style={{
          display: "flex",
          height: "100vh",
        }}
      >
        <Container />
        
      </div>
  );
}

export default App
