import Navbar from "./navbar/NavBar";
import "./navbar/navbar.css";
import InfoView from "./info_view/InfoView";
import AnalyticsView from "./analytics_view/AnalyticsView";
import UserView from "./profile_view/UserView";
import { useState } from "react";
import type { User } from "oidc-client-ts";
import Header from "./header/Header";

interface Props {
  isAuthenticated: boolean;
  canSignIn: boolean;
  user: User | null;
  onSignIn: () => void;
  onSignOut: () => void;
}

const Container = ({
  isAuthenticated,
  canSignIn,
  user,
  onSignIn,
  onSignOut,
}: Props) => {
  // TODO update the menu id logic
  const [selectedMenuId, setSelectedMenuId] = useState("1a");
  return (
    <>
      <Navbar
        isAuthenticated={isAuthenticated}
        canSignIn={canSignIn}
        user={user}
        onSignIn={onSignIn}
        onSignOut={onSignOut}
        selectedMenuId={selectedMenuId}
        setSelectedMenuId={setSelectedMenuId}
      />
      <div style={{ display: "inline" }}>
        <Header/>
        {selectedMenuId == "1a" ? <InfoView /> : null}
        {selectedMenuId == "1e" ? <AnalyticsView /> : null}
        {selectedMenuId == "3a" ? (
          <UserView
            isAuthenticated={isAuthenticated}
            user={user}
            onSignIn={onSignIn}
            onSignOut={onSignOut}
          />
        ) : null}
      </div>
    </>
  );
};

export default Container;
