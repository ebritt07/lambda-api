import { createContext, useContext, useMemo, useState, type ReactNode } from "react";

export type AppAlert = {
  message: string;
  kind: "error" | "success";
};

type AlertContextValue = {
  alert: AppAlert | null;
  setAlert: (alert: AppAlert | null) => void;
};

const AlertContext = createContext<AlertContextValue | undefined>(undefined);

export const AlertProvider = ({ children }: { children: ReactNode }) => {
  const [alert, setAlert] = useState<AppAlert | null>(null);

  const value = useMemo(() => ({ alert, setAlert }), [alert]);

  return <AlertContext.Provider value={value}>{children}</AlertContext.Provider>;
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAlert = (): AlertContextValue => {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error("useAlert must be used within an AlertProvider");
  }
  return context;
};
