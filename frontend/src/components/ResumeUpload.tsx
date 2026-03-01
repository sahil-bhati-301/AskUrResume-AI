import { useState } from "react";
import type { Resume } from "../types";

interface Props {
  onSuccess: (resumes: Resume[]) => void;
}

function ResumeUpload({ onSuccess }: Props) {
  const [files, setFiles] = useState<File[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files).filter((file) =>
        file.name.toLowerCase().endsWith(".pdf"),
      );
      setFiles((prev) => [...prev, ...newFiles]);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFiles = Array.from(e.dataTransfer.files).filter((file) =>
      file.name.toLowerCase().endsWith(".pdf"),
    );
    setFiles((prev) => [...prev, ...droppedFiles]);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setIsUploading(true);
    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await fetch("/api/resumes/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        onSuccess(data);
        setFiles([]);
      } else {
        const error = await response.json();
        alert(`Upload failed: ${error.detail}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload resumes");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        style={{
          border: `2px dashed ${dragOver ? "#007bff" : "#ccc"}`,
          borderRadius: "8px",
          padding: "30px",
          textAlign: "center",
          backgroundColor: dragOver ? "#f0f8ff" : "#fafafa",
          cursor: "pointer",
        }}
      >
        <input
          type="file"
          multiple
          accept=".pdf"
          onChange={handleFileChange}
          id="file-input"
          style={{ display: "none" }}
        />
        <label htmlFor="file-input" style={{ cursor: "pointer" }}>
          <div style={{ fontSize: "40px", marginBottom: "10px" }}>📄</div>
          <p style={{ margin: 0, color: "#666" }}>
            Drag & drop PDF files here, or click to select
          </p>
        </label>
      </div>

      {files.length > 0 && (
        <div style={{ marginTop: "15px" }}>
          <p style={{ fontWeight: "bold", marginBottom: "10px" }}>
            Selected files ({files.length}):
          </p>
          <ul style={{ listStyle: "none", padding: 0 }}>
            {files.map((file, index) => (
              <li
                key={index}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  padding: "8px 12px",
                  backgroundColor: "#f5f5f5",
                  marginBottom: "5px",
                  borderRadius: "4px",
                }}
              >
                <span>{file.name}</span>
                <button
                  onClick={() => removeFile(index)}
                  style={{
                    background: "none",
                    border: "none",
                    color: "#dc3545",
                    cursor: "pointer",
                    fontSize: "18px",
                  }}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            disabled={isUploading}
            style={{
              marginTop: "10px",
              padding: "10px 20px",
              backgroundColor: isUploading ? "#ccc" : "#007bff",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: isUploading ? "not-allowed" : "pointer",
              fontSize: "16px",
            }}
          >
            {isUploading ? "Uploading..." : "Upload Resumes"}
          </button>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
