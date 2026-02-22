import { ColorMap } from "../util/Colors";
import "./HeaderSticker.css";

interface Props {
  text: any;
  stickerType: StickerType;
}

export const StickerType = {
  Info: "Info",
  SuccessAlert: "SuccessAlert",
  ErrorAlert: "ErrorAlert",
} as const;

export type StickerType = typeof StickerType[keyof typeof StickerType];

const StickerTypeColorMap = new Map([
  [StickerType.Info, ColorMap.YELLOW],
  [StickerType.SuccessAlert, ColorMap.GREEN],
  [StickerType.ErrorAlert, ColorMap.PINK],
]);

const HeaderSticker = (props: Props) => {
  const backgroundColor = StickerTypeColorMap.get(props.stickerType);
  return (
    <button
      className="header-sticker"
      style={{ backgroundColor: backgroundColor }}
    >
      {props.text}
    </button>
  );
};

export default HeaderSticker;
