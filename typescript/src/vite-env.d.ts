/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_BUILD_BRANCH?: string;
  readonly VITE_PIPELINE_NUMBER?: string;
  readonly VITE_GITHUB_BASE_URL?: string;
  readonly VITE_GITHUB_REPOSITORY?: string;
  readonly VITE_PIPELINE_RUN_ID?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
