import type { ReactNode } from "react";
import { ColorMap } from "../util/Colors";
import "./HeaderSticker.css";

interface Props {
  text: ReactNode;
  stickerType: StickerType;
  href?: string;
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

  const handleClick = () => {
    if (!props.href) {
      return;
    }

    window.open(props.href, "_blank", "noopener,noreferrer");
  };

  return (
    <button
      type="button"
      className="header-sticker"
      style={{ backgroundColor: backgroundColor }}
      onClick={handleClick}
    >
      {props.text}
    </button>
  );
};

export default HeaderSticker;
