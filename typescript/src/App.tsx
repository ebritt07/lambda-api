import { useAuth } from "react-oidc-context";
import { useEffect, useRef } from "react";
import { isExpectedSignedOutAuthError } from "./auth/authError";
import { useAlert } from "./context/AlertContext";
import Container from './components/Container';

function App() {
  const auth = useAuth();
  const { setAlert } = useAlert();
  const hasAttemptedSilentSignIn = useRef(false);

  useEffect(() => {
    const message = auth.error?.message;
    if (!message) {
      setAlert(null);
      return;
    }

    if (isExpectedSignedOutAuthError(message)) {
      setAlert(null);
      return;
    }

    if (auth.error) {
      setAlert({
        kind: "error",
        message: `Sign-in failed: ${message}`,
      });
      return;
    }

    setAlert(null);
  }, [auth.error, setAlert]);

  useEffect(() => {
    if (hasAttemptedSilentSignIn.current) {
      return;
    }

    if (auth.isLoading || auth.activeNavigator) {
      return;
    }

    if (auth.error || auth.isAuthenticated) {
      hasAttemptedSilentSignIn.current = true;
      return;
    }

    hasAttemptedSilentSignIn.current = true;
    void auth.signinSilent().catch(() => {
      // Expected when there is no existing Cognito session; UI stays signed-out.
    });
  }, [auth.activeNavigator, auth.error, auth.isAuthenticated, auth.isLoading, auth.signinSilent]);

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
