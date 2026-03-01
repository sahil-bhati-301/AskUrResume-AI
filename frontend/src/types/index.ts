export interface Resume {
  id: string;
  filename: string;
  text_preview: string;
  uploaded_at: string;
}

export interface SearchResult {
  id: string;
  filename: string;
  score: number;
  text_preview: string;
}

export interface ResumeListResponse {
  resumes: Resume[];
  total: number;
}
