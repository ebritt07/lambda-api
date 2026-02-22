import DotsButton from "./DotsButton";
import "./navbar.css"
import PlusButton from "./PlusButton";

interface MenuItem {
  name: string;
  emoji: string; // you can set an emoji right in vscode
  id: string;
}

interface Props {
  menuItems: MenuItem[];
  title: string;
  displayMenuButtons: boolean;
  selectedMenuId?: string;
  updateSelectedMenuId: (id: string) => void;
}

const NavBarGroup = (props: Props) => {
  const showColor = "#898989";
  const hideColor = "#f7f7f5";
  const selectedColor = "#EDEDED"

  return (
    <>
      <div className="group-title">
        {props.title}
        <div style={{ marginLeft: "auto", display: "flex" }}>
          <DotsButton
            show={props.displayMenuButtons}
            showColor={showColor}
            hideColor={hideColor}
            handleClick={() => {
              console.log("You clicked the group dots button for " + props.title);
            }}
            id={"test-group-id-" + props.title} // TODO set the id from backend
          />
          <PlusButton
            show={props.displayMenuButtons}
            showColor={showColor}
            hideColor={hideColor}
          />
        </div>
      </div>
      {props.menuItems.map((item: MenuItem) => (
        <div
          className="navbar-item"
          id={item.id}
          style={{
            backgroundColor:
              props.selectedMenuId == item.id ? selectedColor : "",
          }}
          onClick={() => {
            props.updateSelectedMenuId(item.id);
          }}
        >
          {item.emoji}&nbsp;{item.name}
          <div style={{ marginLeft: "auto", display: "flex" }}>
            <DotsButton
              show={props.displayMenuButtons}
              showColor={showColor}
              hideColor={props.selectedMenuId == item.id ? selectedColor : hideColor}
              handleClick={() => {
                console.log("You clicked the dots button for " + item.name);
              }}
              id={"test-subgroup-id-" + item.id} // TODO set the id from backend
            ></DotsButton>
          </div>
        </div>
      ))}
    </>
  );
};

export default NavBarGroup;
