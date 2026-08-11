export interface User {
  id: number;
  username: string;
  email: string;
}

export interface AuthResponse {
  user: User;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface SignupPayload extends LoginPayload {
  email?: string;
}
