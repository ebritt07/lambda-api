## Quick React Template
A quick website demonstration using Vite. It's quite easy to get going!

### Running locally
- `npm i`
- `npm run dev`
### Building for production
- `npm run build`
  - saves production bundle to /dist
- build from branch + pipeline number:
  - `VITE_BUILD_BRANCH="main" VITE_PIPELINE_NUMBER="1234" npm run build`
- optional pipeline link env vars:
  - `VITE_GITHUB_BASE_URL="https://github.com" VITE_GITHUB_REPOSITORY="owner/repo" VITE_PIPELINE_RUN_ID="567890"`
- `npm run preview`
  - serves from the /dist folder
