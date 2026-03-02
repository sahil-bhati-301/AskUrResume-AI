import { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import JobDescriptionInput from "./components/JobDescriptionInput";
import SearchResults from "./components/SearchResults";
import type { Resume, SearchResult } from "./types";

function App() {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  const handleUploadSuccess = (uploadedResumes: Resume[]) => {
    setResumes((prev) => [...prev, ...uploadedResumes]);
  };

  const handleSearch = async (jobDescription: string) => {
    setIsSearching(true);
    setSearchResults([]); // Clear previous results
    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jobDescription, top_k: 3 }),
      });
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "900px",
        margin: "0 auto",
        padding: "20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <h1 style={{ textAlign: "center", color: "#333" }}>
        AURA - AskUrResume-AI
      </h1>
      <p style={{ textAlign: "center", color: "#666", marginBottom: "30px" }}>
        AI-Powered Resume Screening & Matching
      </p>

      <div style={{ marginBottom: "40px" }}>
        <h2
          style={{
            color: "#444",
            borderBottom: "2px solid #eee",
            paddingBottom: "10px",
          }}
        >
          1. Upload Resumes
        </h2>
        <ResumeUpload onSuccess={handleUploadSuccess} />
        {resumes.length > 0 && (
          <p style={{ color: "#28a745", marginTop: "10px" }}>
            {resumes.length} resume(s) uploaded successfully
          </p>
        )}
      </div>

      <div style={{ marginBottom: "40px" }}>
        <h2
          style={{
            color: "#444",
            borderBottom: "2px solid #eee",
            paddingBottom: "10px",
          }}
        >
          2. Enter Job Description
        </h2>
        <JobDescriptionInput
          onSearch={handleSearch}
          isSearching={isSearching}
          hasResumes={resumes.length > 0}
        />
      </div>

      {/* Loading State */}
      {isSearching && (
        <div
          style={{
            textAlign: "center",
            padding: "40px",
            backgroundColor: "#f8f9fa",
            borderRadius: "8px",
            marginBottom: "20px",
          }}
        >
          <div
            style={{
              fontSize: "48px",
              marginBottom: "15px",
            }}
          >
            🤖
          </div>
          <p style={{ fontSize: "16px", color: "#666", margin: 0 }}>
            Analyzing resumes with AI...
          </p>
          <p style={{ fontSize: "14px", color: "#999", marginTop: "8px" }}>
            This may take a few seconds
          </p>
        </div>
      )}

      {/* Results */}
      {searchResults.length > 0 && !isSearching && (
        <div>
          <h2
            style={{
              color: "#444",
              borderBottom: "2px solid #eee",
              paddingBottom: "10px",
            }}
          >
            3. Search Results
          </h2>
          <SearchResults results={searchResults} />
        </div>
      )}
    </div>
  );
}

export default App;
