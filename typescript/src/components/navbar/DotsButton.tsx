import "./buttons.css";

interface Props {
  show: boolean;
  showColor: string;
  hideColor: string;
  handleClick: () => void;
  id: string;
}

const DotsButton = (props: Props) => {

  return (
    <div className="xs-button left" id={props.id} onClick={props.handleClick}>
      <div
        className="dot"
        style={{
          backgroundColor: props.show ? props.showColor : props.hideColor,
        }}
      ></div>
      <div
        className="dot"
        style={{
          backgroundColor: props.show ? props.showColor : props.hideColor,
        }}
      ></div>
      <div
        className="dot"
        style={{
          backgroundColor: props.show ? props.showColor : props.hideColor,
        }}
      ></div>
    </div>
  );
};

export default DotsButton;
