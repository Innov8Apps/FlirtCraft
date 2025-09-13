import React from 'react';
import { ErrorNotification } from './ErrorNotification';
import { useError } from '../../lib/contexts/ErrorContext';

export const ErrorNotificationWrapper: React.FC = () => {
  const { currentError, dismissError } = useError();

  return (
    <ErrorNotification
      message={currentError?.message || ''}
      type={currentError?.type || 'error'}
      isVisible={!!currentError}
      onDismiss={dismissError}
    />
  );
};

export default ErrorNotificationWrapper;