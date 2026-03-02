import type { SearchResult } from "../types";

interface Props {
  results: SearchResult[];
}

function SearchResults({ results }: Props) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "#28a745";
    if (score >= 60) return "#17a2b8";
    if (score >= 40) return "#ffc107";
    return "#dc3545";
  };

  const getScoreLabel = (score: number) => {
    return `${score}% match`;
  };

  return (
    <div>
      <p style={{ marginBottom: "15px", color: "#666" }}>
        Found {results.length} matching resume(s)
      </p>
      <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        {results.map((result, index) => (
          <div
            key={result.id}
            style={{
              border: "1px solid #ddd",
              borderRadius: "8px",
              padding: "20px",
              backgroundColor: "white",
              boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
            }}
          >
            {/* Header */}
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                marginBottom: "15px",
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
                <strong style={{ fontSize: "16px" }}>
                  {result.filename}
                </strong>
              </div>
              {result.match_score && (
                <span
                  style={{
                    padding: "5px 12px",
                    borderRadius: "20px",
                    fontSize: "14px",
                    fontWeight: "bold",
                    color: "white",
                    backgroundColor: getScoreColor(result.match_score),
                  }}
                >
                  {getScoreLabel(result.match_score)}
                </span>
              )}
            </div>

            {/* Summary */}
            {result.summary && (
              <p
                style={{
                  marginBottom: "15px",
                  padding: "12px",
                  backgroundColor: "#f8f9fa",
                  borderRadius: "4px",
                  fontSize: "14px",
                  fontStyle: "italic",
                  color: "#333",
                }}
              >
                {result.summary}
              </p>
            )}

            {/* Strengths */}
            {result.strengths && result.strengths.length > 0 && (
              <div style={{ marginBottom: "12px" }}>
                <strong style={{ color: "#28a745", fontSize: "14px" }}>
                  Strengths:
                </strong>
                <ul
                  style={{
                    marginTop: "5px",
                    paddingLeft: "20px",
                    fontSize: "13px",
                    color: "#555",
                  }}
                >
                  {result.strengths.map((strength, i) => (
                    <li key={i}>{strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Weaknesses */}
            {result.weaknesses && result.weaknesses.length > 0 && (
              <div style={{ marginBottom: "12px" }}>
                <strong style={{ color: "#dc3545", fontSize: "14px" }}>
                  Weaknesses:
                </strong>
                <ul
                  style={{
                    marginTop: "5px",
                    paddingLeft: "20px",
                    fontSize: "13px",
                    color: "#555",
                  }}
                >
                  {result.weaknesses.map((weakness, i) => (
                    <li key={i}>{weakness}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Bias */}
            {result.bias && result.bias.length > 0 && (
              <div>
                <strong style={{ color: "#ffc107", fontSize: "14px" }}>
                  Potential Bias:
                </strong>
                <ul
                  style={{
                    marginTop: "5px",
                    paddingLeft: "20px",
                    fontSize: "13px",
                    color: "#555",
                  }}
                >
                  {result.bias.map((bias, i) => (
                    <li key={i}>{bias}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchResults;
