import HeaderSticker, { StickerType } from "./HeaderSticker";

const Header = () => {
  return (
    <div className="header">
      <div style={{ display: "flex" }}>
        <h2>Lambda UI</h2>
        <HeaderSticker
          text="development"
          stickerType={StickerType.Info}
        />
        {/* Add a functionality to show alert when alert context is updated */}
      </div>
    </div>
  );
};

export default Header;
