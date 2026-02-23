import { useAuth } from "react-oidc-context";
import type { User } from "oidc-client-ts";
import { buildCognitoSignOutUrl } from "./auth/cognitoConfig";
import Container from './components/Container';

function App() {
  const auth = useAuth();

  const handleSignIn = () => {
    void auth.signinRedirect();
  };

  const handleSignOut = () => {
    void auth.removeUser();
    window.location.href = buildCognitoSignOutUrl();
  };

  const user: User | null = auth.user ?? null;
  const isAuthenticated = Boolean(auth.isAuthenticated && user);
  const canSignIn = auth.activeNavigator === undefined && !auth.isLoading;

return (
      <div
        className="app"
        style={{
          display: "flex",
          height: "100vh",
        }}
      >
        <Container
          isAuthenticated={isAuthenticated}
          canSignIn={canSignIn}
          user={user}
          onSignIn={handleSignIn}
          onSignOut={handleSignOut}
        />
        
      </div>
  );
}

export default App
