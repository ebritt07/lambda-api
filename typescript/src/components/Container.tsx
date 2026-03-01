import Navbar from "./navbar/NavBar";
import "./navbar/navbar.css";
import InfoView from "./info_view/InfoView";
import AnalyticsView from "./analytics_view/AnalyticsView";
import UserView from "./profile_view/UserView";
import { useState } from "react";
import Header from "./header/Header";

const Container = () => {
  // TODO update the menu id logic
  const [selectedMenuId, setSelectedMenuId] = useState("1a");
  return (
    <>
      <Navbar
        selectedMenuId={selectedMenuId}
        setSelectedMenuId={setSelectedMenuId}
      />
      <div style={{ display: "inline" }}>
        <Header />
        {selectedMenuId == "1a" ? <InfoView /> : null}
        {selectedMenuId == "1e" ? <AnalyticsView /> : null}
        {selectedMenuId == "3a" ? <UserView /> : null}
      </div>
    </>
  );
};

export default Container;
