import HeaderSticker, { StickerType } from "./HeaderSticker";

const getPipelineUrl = (): string | undefined => {
  const baseUrl = import.meta.env.VITE_GITHUB_BASE_URL?.trim() || "https://github.com";
  const repository = import.meta.env.VITE_GITHUB_REPOSITORY?.trim();
  const runId = import.meta.env.VITE_PIPELINE_RUN_ID?.trim();

  if (!repository || !runId) {
    return undefined;
  }

  return `${baseUrl}/${repository}/actions/runs/${runId}`;
};

const getBuildLabel = (): string => {
  const branch = import.meta.env.VITE_BUILD_BRANCH?.trim();
  const pipelineNumber = import.meta.env.VITE_PIPELINE_NUMBER?.trim();

  if (branch && pipelineNumber) {
    return `${branch}-${pipelineNumber}`;
  }

  if (branch) {
    return branch;
  }

  if (pipelineNumber) {
    return `pipeline ${pipelineNumber}`;
  }

  return "development";
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
