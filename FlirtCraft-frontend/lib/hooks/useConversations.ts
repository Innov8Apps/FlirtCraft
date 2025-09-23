import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { conversationService } from '../api/services/conversationService';
import {
  Conversation,
  CreateConversationRequest,
  SendMessageRequest,
  CompleteConversationRequest,
  GenerateContextRequest,
} from '../api/types';

// Query keys
export const conversationKeys = {
  all: ['conversations'] as const,
  lists: () => [...conversationKeys.all, 'list'] as const,
  list: (filters: Record<string, any>) => [...conversationKeys.lists(), { filters }] as const,
  details: () => [...conversationKeys.all, 'detail'] as const,
  detail: (id: string) => [...conversationKeys.details(), id] as const,
  feedback: (id: string) => [...conversationKeys.detail(id), 'feedback'] as const,
  context: (params: GenerateContextRequest) => ['context', params] as const,
};

// Get all conversations
export const useConversations = () => {
  return useQuery({
    queryKey: conversationKeys.lists(),
    queryFn: conversationService.getConversations,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

// Get specific conversation
export const useConversation = (id: string) => {
  return useQuery({
    queryKey: conversationKeys.detail(id),
    queryFn: () => conversationService.getConversation(id),
    enabled: !!id,
    staleTime: 2 * 60 * 1000, // 2 minutes for active conversations
  });
};

// Get conversation feedback
export const useConversationFeedback = (conversationId: string) => {
  return useQuery({
    queryKey: conversationKeys.feedback(conversationId),
    queryFn: () => conversationService.getFeedback(conversationId),
    enabled: !!conversationId,
    staleTime: 10 * 60 * 1000, // 10 minutes - feedback doesn't change
  });
};

// Get conversation history
export const useConversationHistory = (limit?: number) => {
  return useQuery({
    queryKey: conversationKeys.list({ limit, status: 'completed' }),
    queryFn: () => conversationService.getConversationHistory(limit),
    staleTime: 5 * 60 * 1000,
  });
};

// Create new conversation
export const useCreateConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateConversationRequest) => conversationService.createConversation(data),
    onSuccess: (newConversation) => {
      // Add to conversations list
      queryClient.setQueryData(conversationKeys.lists(), (old: Conversation[] | undefined) => {
        return old ? [newConversation, ...old] : [newConversation];
      });

      // Set individual conversation data
      queryClient.setQueryData(conversationKeys.detail(newConversation.id), newConversation);
    },
    onError: (error) => {
      console.error('Failed to create conversation:', error);
    },
  });
};

// Send message
export const useSendMessage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ conversationId, data }: { conversationId: string; data: SendMessageRequest }) =>
      conversationService.sendMessage(conversationId, data),
    onSuccess: (response, { conversationId }) => {
      // Update the conversation with new messages
      queryClient.setQueryData(conversationKeys.detail(conversationId), (old: Conversation | undefined) => {
        if (!old) return old;

        const updatedMessages = [...(old.messages || [])];
        updatedMessages.push(response.message);
        if (response.ai_response) {
          updatedMessages.push(response.ai_response);
        }

        return {
          ...old,
          messages: updatedMessages,
          total_messages: updatedMessages.length,
        };
      });

      // Invalidate conversations list to update message counts
      queryClient.invalidateQueries({ queryKey: conversationKeys.lists() });
    },
    onError: (error) => {
      console.error('Failed to send message:', error);
    },
  });
};

// Complete conversation
export const useCompleteConversation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ conversationId, data }: { conversationId: string; data?: CompleteConversationRequest }) =>
      conversationService.completeConversation(conversationId, data),
    onSuccess: (updatedConversation) => {
      // Update the conversation data
      queryClient.setQueryData(conversationKeys.detail(updatedConversation.id), updatedConversation);

      // Update conversations list
      queryClient.setQueryData(conversationKeys.lists(), (old: Conversation[] | undefined) => {
        if (!old) return old;
        return old.map((conversation) =>
          conversation.id === updatedConversation.id ? updatedConversation : conversation
        );
      });

      // Invalidate user stats as they might have changed
      queryClient.invalidateQueries({ queryKey: ['user', 'stats'] });
    },
    onError: (error) => {
      console.error('Failed to complete conversation:', error);
    },
  });
};

// Generate conversation context
export const useGenerateContext = () => {
  return useMutation({
    mutationFn: (data: GenerateContextRequest) => conversationService.generateContext(data),
    onError: (error) => {
      console.error('Failed to generate context:', error);
    },
  });
};