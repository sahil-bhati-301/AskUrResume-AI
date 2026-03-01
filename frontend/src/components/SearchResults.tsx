import type { SearchResult } from "../types";

interface Props {
  results: SearchResult[];
}

function SearchResults({ results }: Props) {
  const getScoreColor = (score: number) => {
    if (score >= 0.8) return "#28a745"; // green
    if (score >= 0.6) return "#17a2b8"; // blue
    if (score >= 0.4) return "#ffc107"; // yellow
    return "#dc3545"; // red
  };

  const getScoreLabel = (score: number) => {
    return `${(score * 100).toFixed(1)}% match`;
  };

  return (
    <div>
      <p style={{ marginBottom: "15px", color: "#666" }}>
        Found {results.length} matching resume(s)
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
        {results.map((result, index) => (
          <div
            key={result.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "15px",
              backgroundColor: "white",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
              }}
            >
              <div>
                <span
                  style={{
                    display: "inline-block",
                    width: "24px",
                    height: "24px",
                    lineHeight: "24px",
                    textAlign: "center",
                    backgroundColor: "#f0f0f0",
                    borderRadius: "50%",
                    marginRight: "10px",
                    fontSize: "12px",
                  }}
                >
                  {index + 1}
                </span>
                <strong style={{ fontSize: "16px" }}>{result.filename}</strong>
              </div>
              <span
                style={{
                  padding: "5px 10px",
                  borderRadius: "20px",
                  fontSize: "14px",
                  fontWeight: "bold",
                  color: "white",
                  backgroundColor: getScoreColor(result.score),
                }}
              >
                {getScoreLabel(result.score)}
              </span>
            </div>
            <p
              style={{
                marginTop: "10px",
                padding: "10px",
                backgroundColor: "#f9f9f9",
                borderRadius: "4px",
                fontSize: "13px",
                color: "#555",
              }}
            >
              {result.text_preview}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchResults;
