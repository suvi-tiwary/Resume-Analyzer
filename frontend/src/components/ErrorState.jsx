import { AlertTriangle, RotateCcw } from "lucide-react";

export default function ErrorState({ error, onRetry }) {
  return (
    <div className="error-screen">
      <div className="error-card">
        <div className="error-icon-box">
          <AlertTriangle size={32} />
        </div>

        <h2 className="error-title">Unable to analyze resume</h2>

        <p className="error-message">
          {error ||
            "Something went wrong while processing your file. Please try again."}
        </p>

        <button
          className="try-again-button"
          onClick={onRetry}
          type="button"
          aria-label="Try again"
        >
          <RotateCcw size={16} />
          <span>Try Again</span>
        </button>
      </div>
    </div>
  );
}
