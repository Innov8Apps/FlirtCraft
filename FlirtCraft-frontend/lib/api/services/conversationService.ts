import apiClient from '../client';
import {
  Conversation,
  CreateConversationRequest,
  SendMessageRequest,
  SendMessageResponse,
  CompleteConversationRequest,
  FeedbackMetrics,
  ConversationContext,
  GenerateContextRequest,
} from '../types';

export class ConversationService {
  // Get all conversations for the current user
  async getConversations(): Promise<Conversation[]> {
    return apiClient.get<Conversation[]>('/conversations');
  }

  // Get a specific conversation by ID
  async getConversation(id: string): Promise<Conversation> {
    return apiClient.get<Conversation>(`/conversations/${id}`);
  }

  // Create a new conversation
  async createConversation(data: CreateConversationRequest): Promise<Conversation> {
    return apiClient.post<Conversation>('/conversations', data);
  }

  // Send a message in a conversation
  async sendMessage(conversationId: string, data: SendMessageRequest): Promise<SendMessageResponse> {
    return apiClient.post<SendMessageResponse>(`/conversations/${conversationId}/messages`, data);
  }

  // Complete a conversation
  async completeConversation(conversationId: string, data?: CompleteConversationRequest): Promise<Conversation> {
    return apiClient.put<Conversation>(`/conversations/${conversationId}/complete`, data);
  }

  // Get conversation feedback
  async getFeedback(conversationId: string): Promise<FeedbackMetrics> {
    return apiClient.get<FeedbackMetrics>(`/conversations/${conversationId}/feedback`);
  }

  // Generate pre-conversation context
  async generateContext(data: GenerateContextRequest): Promise<ConversationContext> {
    return apiClient.post<ConversationContext>('/conversations/context', data);
  }

  // Get conversation history (last N conversations)
  async getConversationHistory(limit: number = 10): Promise<Conversation[]> {
    return apiClient.get<Conversation[]>('/conversations', { limit, status: 'completed' });
  }
}

export const conversationService = new ConversationService();