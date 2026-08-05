import { createContext, useContext, useState, useCallback } from "react";

import API from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem("visioniq_user");
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  });

  // ==========================================
  // Login
  // ==========================================

  const login = useCallback(async (username, password) => {
    const form = new URLSearchParams({
      username,
      password,
    });

    const response = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: form.toString(),
    });

    if (!response.ok) {
      let errorMessage = "Login failed";

      try {
        const err = await response.json();
        errorMessage = err.detail || errorMessage;
      } catch {
        // Ignore JSON parsing errors
      }

      throw new Error(errorMessage);
    }

    const data = await response.json();

    const profile = {
      ...data.user,
      token: data.access_token,
    };

    localStorage.setItem(
      "visioniq_user",
      JSON.stringify(profile)
    );

    setUser(profile);

    return profile;
  }, []);

  // ==========================================
  // Logout
  // ==========================================

  const logout = useCallback(() => {
    localStorage.removeItem("visioniq_user");
    setUser(null);
  }, []);

  // ==========================================
  // Permission Check
  // ==========================================

  const can = useCallback(
    (page) => {
      return user?.permissions?.includes(page) ?? false;
    },
    [user]
  );

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        can,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}