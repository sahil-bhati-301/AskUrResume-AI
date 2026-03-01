import { useState } from "react";

interface Props {
  onSearch: (jobDescription: string) => void;
  isSearching: boolean;
  hasResumes: boolean;
}

function JobDescriptionInput({ onSearch, isSearching, hasResumes }: Props) {
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (description.trim() && !isSearching) {
      onSearch(description);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter job description here... (e.g., We are looking for a Python developer with experience in machine learning and data analysis)"
          disabled={isSearching || !hasResumes}
          style={{
            width: "100%",
            height: "150px",
            padding: "12px",
            fontSize: "14px",
            fontFamily: "Arial, sans-serif",
            border: "1px solid #ccc",
            borderRadius: "4px",
            resize: "vertical",
            boxSizing: "border-box",
          }}
        />
        <button
          type="submit"
          disabled={isSearching || !hasResumes || !description.trim()}
          style={{
            marginTop: "10px",
            padding: "10px 20px",
            backgroundColor:
              isSearching || !hasResumes || !description.trim()
                ? "#ccc"
                : "#28a745",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor:
              isSearching || !hasResumes || !description.trim()
                ? "not-allowed"
                : "pointer",
            fontSize: "16px",
          }}
        >
          {isSearching ? "Searching..." : "Find Matching Resumes"}
        </button>
      </form>
      {!hasResumes && (
        <p style={{ color: "#dc3545", marginTop: "10px" }}>
          Please upload resumes first before searching
        </p>
      )}
    </div>
  );
}

export default JobDescriptionInput;
