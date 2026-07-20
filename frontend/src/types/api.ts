// ─── Auth ──────────────────────────────────────────────

export interface LoginRequest {
  username: string;
  email?: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  tokens: AuthTokens;
  user: UserInfo;
}

export interface RegisterResponse {
  tokens: AuthTokens;
  user: UserInfo;
}

export interface UserInfo {
  id: number;
  username: string;
  email: string;
}

// ─── Profile / Dashboard ──────────────────────────────

export interface UserProfile {
  username: string;
  email: string;
  questions_attempted: number;
  questions_solved: number;
  current_streak: number;
  longest_streak: number;
  last_practice_date: string | null;
}

export interface DashboardData {
  username: string;
  questions_attempted: number;
  questions_solved: number;
  current_streak: number;
  longest_streak: number;
  last_practice_date: string | null;
}

// ─── Roles & Topics ───────────────────────────────────

export interface Role {
  id: number;
  name: string;
  slug: string;
  description: string;
  topic_count: number;
}

export interface Topic {
  id: number;
  name: string;
  short_name: string;
  icon: string;
  role: number;
  order: number;
  question_count: number;
  difficulty_breakdown: {
    easy: number;
    medium: number;
    hard: number;
  };
}

// ─── Problems ─────────────────────────────────────────

export type Difficulty = 'easy' | 'medium' | 'hard';
export type QuestionType = 'mcq' | 'coding';

export interface ProblemSummary {
  id: number;
  title: string;
  slug: string;
  difficulty: Difficulty;
  question_type: QuestionType;
  topic_name: string;
  role_name: string;
  role_slug: string;
  user_solved?: boolean;
  user_attempted?: boolean;
}

export interface AnswerOption {
  id: number;
  text: string;
  order: number;
}

export interface StarterCode {
  python_code: string;
}

export interface TestCase {
  id: number;
  stdin: string;
  expected_output: string;
  is_hidden: boolean;
  order: number;
}

export interface ProblemDetail {
  id: number;
  title: string;
  slug: string;
  text: string;
  explanation: string;
  difficulty: Difficulty;
  question_type: QuestionType;
  topic_name: string;
  role_name: string;
  options: AnswerOption[];
  starter_code: StarterCode | null;
  test_cases: TestCase[];
}

// ─── Code Execution ───────────────────────────────────

export interface CodeRunRequest {
  slug: string;
  code: string;
  language: string;
}

export interface CodeRunResponse {
  task_id: string;
}

export interface CodeSubmitRequest {
  code: string;
  language: string;
}

export interface CodeSubmitResponse {
  task_id: string;
  attempt_id: number;
}

export interface TestCaseResult {
  passed: boolean;
  output: string;
  expected: string;
  error: string;
  status: string;
  truncated: boolean;
  time?: string;
}

export interface TaskResultData {
  results?: TestCaseResult[];
  error?: string;
  traceback?: string;
  _sentinel?: string;
  attempt_id?: number;
  verdict?: string;
  question_id?: number;
}

export interface TaskResultResponse {
  task_id: string;
  status: 'PENDING' | 'SUCCESS' | 'FAILURE';
  result: TaskResultData | string;
}

// ─── Exams ────────────────────────────────────────────

export type ExamMode = 'full_mock' | 'category_drill';

export interface ExamStartRequest {
  mode: ExamMode;
  role?: string | null;
}

export interface ExamSession {
  id: number;
  mode: ExamMode;
  role: number | null;
  started_at: string;
  finished_at: string | null;
  score: number | null;
  total_questions: number;
  is_completed: boolean;
  is_expired: boolean;
}

export interface ExamDetail {
  session: ExamSession;
  questions: ExamQuestion[];
}

export interface ExamQuestion {
  id: number;
  question: ProblemDetail;
  answer: UserAttemptSummary | null;
  order: number;
}

export interface UserAttemptSummary {
  id: number;
  verdict: string;
  is_correct: boolean;
  execution_time_ms: number;
  created_at: string;
}

export interface ExamAnswerRequest {
  question_id: number;
  selected_option_id: number;
}

export interface ExamAnswerResponse {
  is_correct: boolean;
  correct_option_id?: number;
  explanation?: string;
}

export interface ExamFinishResponse {
  id: number;
  mode: ExamMode;
  score: number;
  total_questions: number;
  is_completed: boolean;
}

export interface ExamResults {
  id: number;
  mode: ExamMode;
  started_at: string;
  finished_at: string;
  score: number;
  total_questions: number;
  questions: ExamResultQuestion[];
}

export interface ExamResultQuestion {
  id: number;
  question: ProblemSummary & { options: AnswerOption[]; explanation: string };
  answer: UserAttemptSummary | null;
  order: number;
}

export interface ExamHistoryItem {
  id: number;
  mode: ExamMode;
  started_at: string;
  finished_at: string | null;
  score: number | null;
  total_questions: number;
  is_completed: boolean;
}

// ─── Config ───────────────────────────────────────────

export interface AppConfig {
  enabled_languages: string[];
}

// ─── API Error ────────────────────────────────────────

export interface ApiError {
  error: boolean;
  status_code: number;
  detail: string | Record<string, string[]>;
}
