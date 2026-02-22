import { useState } from "react";
import NavBarGroup from "./NavBarGroup";
import "./navbar.css";

interface Props {
  selectedMenuId: string;
  setSelectedMenuId: (id: string) => void;
}

const Navbar = (props: Props) => {

  const bicycleMenuItems = [
    {"name": "Info", emoji:"📚", "id": "1a"},
    {"name": "Data Table", emoji:"📊", "id": "1b"},
  ]

  const adminMenuItems = [
    {"name": "Admin Info", emoji:"📚", "id": "2a"},
    {"name": "Admin Table", emoji:"📊", "id": "2b"},
  ]

  const [mouseInNavBar, setMouseInNavBar] = useState(false);

  const handleMouseEnter = () => {
    setMouseInNavBar(true);
  };

  const handleMouseLeave = () => {
    setMouseInNavBar(false);
  };

  return (
    <div
      className="navbar"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="nav-panel">
        <div>
          <h5>
            <i style={{ paddingLeft: "30px" }}>@username</i>
          </h5>
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
      </div>
    </div>
  );
};

export default Navbar;
