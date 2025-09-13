import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

export interface ErrorNotification {
  id: string;
  message: string;
  type?: 'error' | 'warning' | 'info';
  duration?: number;
}

interface ErrorContextValue {
  currentError: ErrorNotification | null;
  showError: (message: string, type?: 'error' | 'warning' | 'info', duration?: number) => void;
  dismissError: () => void;
  dismissErrorOnNavigation: () => void;
}

const ErrorContext = createContext<ErrorContextValue | undefined>(undefined);

interface ErrorProviderProps {
  children: ReactNode;
}

export const ErrorProvider: React.FC<ErrorProviderProps> = ({ children }) => {
  const [currentError, setCurrentError] = useState<ErrorNotification | null>(null);
  const [timeoutId, setTimeoutId] = useState<ReturnType<typeof setTimeout> | null>(null);

  const dismissError = useCallback(() => {
    setCurrentError(null);
    if (timeoutId) {
      clearTimeout(timeoutId);
      setTimeoutId(null);
    }
  }, [timeoutId]);

  const showError = useCallback((
    message: string,
    type: 'error' | 'warning' | 'info' = 'error',
    duration: number = 0
  ) => {
    // Clear any existing timeout
    if (timeoutId) {
      clearTimeout(timeoutId);
    }

    // Create new error
    const newError: ErrorNotification = {
      id: Date.now().toString(),
      message,
      type,
      duration,
    };

    setCurrentError(newError);

    // Auto-dismiss after duration
    if (duration > 0) {
      const newTimeoutId = setTimeout(() => {
        setCurrentError(null);
        setTimeoutId(null);
      }, duration);
      setTimeoutId(newTimeoutId);
    }
  }, [timeoutId]);

  const dismissErrorOnNavigation = useCallback(() => {
    // Only dismiss if there's an error showing
    if (currentError) {
      dismissError();
    }
  }, [currentError, dismissError]);

  const contextValue: ErrorContextValue = {
    currentError,
    showError,
    dismissError,
    dismissErrorOnNavigation,
  };

  return (
    <ErrorContext.Provider value={contextValue}>
      {children}
    </ErrorContext.Provider>
  );
};

export const useError = (): ErrorContextValue => {
  const context = useContext(ErrorContext);
  if (!context) {
    throw new Error('useError must be used within an ErrorProvider');
  }
  return context;
};