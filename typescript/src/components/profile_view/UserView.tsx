import { useMemo, useState } from "react";
import type { User } from "oidc-client-ts";
import { useAuth } from "react-oidc-context";
import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { buildCognitoSignOutUrl } from "../../auth/cognitoConfig";

const getProfileTextValue = (user: User | null, key: string): string => {
  const value = user?.profile[key];
  if (typeof value === "string" && value.trim() !== "") {
    return value;
  }
  return "";
};

const getProfileBooleanValue = (user: User | null, key: string): string => {
  const value = user?.profile[key];
  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }
  if (typeof value === "string" && (value === "true" || value === "false")) {
    return value;
  }
  return "";
};

const getUnixSecondsAsDate = (user: User | null, key: string): string => {
  const value = user?.profile[key];
  const parsed = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return "";
  }
  return new Date(parsed * 1000).toLocaleString();
};

interface UserFieldRow {
  field: string;
  value: string;
}

const UserView = () => {
  const auth = useAuth();
  const user: User | null = auth.user ?? null;
  const isAuthenticated = Boolean(auth.isAuthenticated && user);
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "failed">("idle");
  const userRows = useMemo<UserFieldRow[]>(
    () => [
      { field: "Username", value: getProfileTextValue(user, "cognito:username") },
      { field: "Email", value: getProfileTextValue(user, "email") },
      { field: "Email Verified", value: getProfileBooleanValue(user, "email_verified") },
      { field: "Logged In Since", value: getUnixSecondsAsDate(user, "iat") },
      { field: "Session Ends At", value: getUnixSecondsAsDate(user, "exp") },
    ],
    [user],
  );

  const columns = useMemo<ColumnDef<UserFieldRow>[]>(
    () => [
      { header: "Field", accessorKey: "field" },
      { header: "Value", accessorKey: "value" },
    ],
    [],
  );

  const table = useReactTable({
    data: userRows,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const handleCopyToken = async () => {
    if (!user?.access_token) {
      setCopyStatus("failed");
      return;
    }

    try {
      await navigator.clipboard.writeText(user.access_token);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
  };

  const handleSignIn = () => {
    void auth.signinRedirect();
  };

  const handleSignOut = () => {
    void auth.removeUser();
    window.location.href = buildCognitoSignOutUrl();
  };

  return (
    <div className="info-view">
      <p>Check out your profile information.</p>

      {isAuthenticated ? (
        <div style={{ border: "1px solid #d8d8d8", borderRadius: "6px", padding: "12px", marginBottom: "16px" }}>
          <h4 style={{ marginTop: 0, marginBottom: "10px" }}>User Details</h4>
          <table style={{ borderCollapse: "collapse", width: "100%" }}>
            <thead>
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      key={header.id}
                      style={{ textAlign: "left", borderBottom: "1px solid #ddd", padding: "8px" }}
                    >
                      {header.isPlaceholder
                        ? null
                        : flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} style={{ borderBottom: "1px solid #eee", padding: "8px" }}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
      {isAuthenticated ? (
        <p>
          <button type="button" onClick={() => { void handleCopyToken(); }}>
            Copy Access Token
          </button>
          <span className="profile-token-status">
            {copyStatus === "copied" ? " Copied" : copyStatus === "failed" ? " Unable to copy" : ""}
          </span>
        </p>
      ) : null}
      {isAuthenticated ? (
        <button type="button" onClick={handleSignOut}>
          Sign Out
        </button>
      ) : (
        <button type="button" onClick={handleSignIn}>
          Sign In
        </button>
      )}
    </div>
  );
};

export default UserView;
