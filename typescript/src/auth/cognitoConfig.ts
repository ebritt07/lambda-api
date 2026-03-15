import { isDevelopmentBuild } from "../config/buildInfo";

const COGNITO_AUTHORITY = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_6IDvYI8kL";
const COGNITO_CLIENT_ID = "47vcr069758ouq7uk95r532b41";
const COGNITO_DOMAIN = "https://us-east-16idvyi8kl.auth.us-east-1.amazoncognito.com";

const getRedirectUri = (): string =>
  isDevelopmentBuild() ? "http://localhost:5173/" : "https://ebritt07.click";

export const cognitoAuthConfig = {
  authority: COGNITO_AUTHORITY,
  client_id: COGNITO_CLIENT_ID,
  redirect_uri: getRedirectUri(),
  response_type: "code",
  scope: "openid email phone ebritt07.click/bike.modify",
};

export const buildCognitoSignOutUrl = (): string => {
  const logoutUri = getRedirectUri();
  return `${COGNITO_DOMAIN}/logout?client_id=${COGNITO_CLIENT_ID}&logout_uri=${encodeURIComponent(logoutUri)}`;
};
