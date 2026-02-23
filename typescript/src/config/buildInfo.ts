const getTrimmed = (value: string | undefined): string => value?.trim() ?? "";

export const getBuildLabel = (): string => {
  const branch = getTrimmed(import.meta.env.VITE_BUILD_BRANCH);
  const pipelineNumber = getTrimmed(import.meta.env.VITE_PIPELINE_NUMBER);

  if (branch && pipelineNumber) {
    return `${branch}-${pipelineNumber}`;
  }

  return "development";
};

export const isDevelopmentBuild = (): boolean => getBuildLabel() === "development";
