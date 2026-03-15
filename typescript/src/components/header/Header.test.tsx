import { render, screen } from "@testing-library/react";
import { useEffect } from "react";
import { describe, expect, it } from "vitest";
import Header from "./Header";
import { AlertProvider, useAlert } from "../../context/AlertContext";

const AlertSeeder = ({ message }: { message: string }) => {
  const { setAlert } = useAlert();
  useEffect(() => {
    setAlert({ kind: "error", message });
  }, [message, setAlert]);
  return null;
};

describe("Header", () => {
  it("shows alert message from AlertContext", () => {
    render(
      <AlertProvider>
        <AlertSeeder message="Sign-in failed: invalid response" />
        <Header />
      </AlertProvider>,
    );

    expect(screen.getByText("Sign-in failed: invalid response")).toBeInTheDocument();
  });
});
