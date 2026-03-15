import { describe, expect, it } from "vitest";
import { isExpectedSignedOutAuthError } from "./authError";

describe("isExpectedSignedOutAuthError", () => {
  it("returns true for login_required style messages", () => {
    expect(isExpectedSignedOutAuthError("login_required")).toBe(true);
    expect(isExpectedSignedOutAuthError("Sign in failed: Login required")).toBe(true);
  });

  it("returns false for unexpected errors", () => {
    expect(isExpectedSignedOutAuthError("invalid_scope")).toBe(false);
    expect(isExpectedSignedOutAuthError("network timeout")).toBe(false);
  });
});
