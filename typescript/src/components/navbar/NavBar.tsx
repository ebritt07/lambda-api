import { useState } from "react";
import { useAuth } from "react-oidc-context";
import NavBarGroup from "./NavBarGroup";
import "./navbar.css";

interface Props {
  selectedMenuId: string;
  setSelectedMenuId: (id: string) => void;
}

const Navbar = (props: Props) => {
  const auth = useAuth();

  const bicycleMenuItems = [
    { "name": "Info", emoji: "📚", "id": "1a" },
    { "name": "Data Table", emoji: "📊", "id": "1b" },
  ]

  const adminMenuItems = [
    { "name": "Admin Info", emoji: "📚", "id": "2a" },
    { "name": "Admin Table", emoji: "📊", "id": "2b" },
  ]

  const profileMenuItems = [
    { "name": "User", emoji: "👤", "id": "3a" },
  ]

  const [mouseInNavBar, setMouseInNavBar] = useState(false);

  const handleMouseEnter = () => {
    setMouseInNavBar(true);
  };

  const handleMouseLeave = () => {
    setMouseInNavBar(false);
  };

  const toNonEmptyString = (value: unknown): string | undefined =>
    typeof value === "string" && value.trim() !== "" ? value : undefined;

  const userLabel = auth.user?.profile["cognito:username"]
    ? toNonEmptyString(auth.user.profile["cognito:username"])
    : undefined;
  const fallbackUserLabel = toNonEmptyString(auth.user?.profile.preferred_username)
    || toNonEmptyString(auth.user?.profile.sub)
    || "username";
  const resolvedUserLabel = (userLabel || fallbackUserLabel).replace(/^@+/, "");
  const isAuthenticated = Boolean(auth.isAuthenticated && auth.user);

  return (
    <div
      className="navbar"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="nav-panel">
        <div>

          <h5><i style={{ paddingLeft: "30px" }}>{isAuthenticated ? `@${resolvedUserLabel}` : "@username"}</i></h5>
        </div>

        <NavBarGroup
          menuItems={bicycleMenuItems}
          displayMenuButtons={mouseInNavBar}
          title="Bicycle Lambda"
          selectedMenuId={props.selectedMenuId}
          updateSelectedMenuId={props.setSelectedMenuId}
        />

        <NavBarGroup
          menuItems={adminMenuItems}
          displayMenuButtons={mouseInNavBar}
          title="Admin Lambda"
          selectedMenuId={props.selectedMenuId}
          updateSelectedMenuId={props.setSelectedMenuId}
        />
        <NavBarGroup
          menuItems={profileMenuItems}
          displayMenuButtons={mouseInNavBar}
          title="My Profile"
          selectedMenuId={props.selectedMenuId}
          updateSelectedMenuId={props.setSelectedMenuId}
        />
      </div>
    </div>
  );
};

export default Navbar;
