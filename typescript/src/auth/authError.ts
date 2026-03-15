export const isExpectedSignedOutAuthError = (message: string): boolean => {
  const normalized = message.toLowerCase();
  return normalized.includes("login required") || normalized.includes("login_required");
};
