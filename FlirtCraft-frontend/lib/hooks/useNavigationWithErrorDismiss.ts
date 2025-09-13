import { useError } from '../contexts/ErrorContext';
import { useCallback } from 'react';

/**
 * Hook that combines navigation with automatic error dismissal
 * Use this for navigation buttons that should dismiss error notifications
 */
export const useNavigationWithErrorDismiss = () => {
  const { dismissErrorOnNavigation } = useError();

  const navigateWithDismiss = useCallback((navigationAction: () => void) => {
    dismissErrorOnNavigation();
    navigationAction();
  }, [dismissErrorOnNavigation]);

  return {
    navigateWithDismiss,
    dismissErrorOnNavigation,
  };
};

export default useNavigationWithErrorDismiss;