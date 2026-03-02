export interface Resume {
  id: string
  filename: string
  text_preview: string
  uploaded_at: string
}

export interface SearchResult {
  id: string
  filename: string
  score: number
  text_preview: string
  // LLM evaluation fields
  match_score?: number
  strengths?: string[]
  weaknesses?: string[]
  bias?: string[]
  summary?: string
}

export interface ResumeListResponse {
  resumes: Resume[]
  total: number
}
