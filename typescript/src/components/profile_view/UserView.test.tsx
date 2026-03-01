import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import UserView from "./UserView";

const useAuthMock = vi.fn();

vi.mock("react-oidc-context", () => ({
  useAuth: () => useAuthMock(),
}));

vi.mock("../../auth/cognitoConfig", () => ({
  buildCognitoSignOutUrl: () => "https://example.com/logout",
}));

describe("UserView", () => {
  it("shows sign-in action when user is not authenticated", () => {
    useAuthMock.mockReturnValue({
      user: null,
      isAuthenticated: false,
      signinRedirect: vi.fn(),
      removeUser: vi.fn(),
    });

    render(<UserView />);

    expect(screen.getByRole("button", { name: "Sign In" })).toBeInTheDocument();
    expect(screen.queryByText("User Details")).not.toBeInTheDocument();
  });

  it("shows table values when user is authenticated", () => {
    useAuthMock.mockReturnValue({
      user: {
        access_token: "token-123",
        profile: {
          "cognito:username": "jane",
          email: "jane@example.com",
          email_verified: true,
          iat: 1700000000,
          exp: 1700003600,
        },
      },
      isAuthenticated: true,
      signinRedirect: vi.fn(),
      removeUser: vi.fn(),
    });

    render(<UserView />);

    expect(screen.getByText("User Details")).toBeInTheDocument();
    expect(screen.getByText("jane")).toBeInTheDocument();
    expect(screen.getByText("jane@example.com")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Sign Out" })).toBeInTheDocument();
  });
});
