import HeaderSticker, { StickerType } from "./HeaderSticker";
import { getBuildLabel } from "../../config/buildInfo";

const getPipelineUrl = (): string | undefined => {
  const baseUrl = import.meta.env.VITE_GITHUB_BASE_URL?.trim() || "https://github.com";
  const repository = import.meta.env.VITE_GITHUB_REPOSITORY?.trim();
  const runId = import.meta.env.VITE_PIPELINE_RUN_ID?.trim();

  if (!repository || !runId) {
    return undefined;
  }

  return `${baseUrl}/${repository}/actions/runs/${runId}`;
};

const Header = () => {
  const buildLabel = getBuildLabel();
  const pipelineUrl = getPipelineUrl();

  return (
    <div className="header">
      <div style={{ display: "flex" }}>
        <h2>Lambda UI</h2>
        <HeaderSticker
          text={buildLabel}
          stickerType={StickerType.Info}
          href={pipelineUrl}
        />
        {/* Add a functionality to show alert when alert context is updated */}
      </div>
    </div>
  );
};

export default Header;
