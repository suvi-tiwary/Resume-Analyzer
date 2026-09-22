import { useState, useEffect } from "react";
import {
  FileText,
  FileImage,
  Sparkles,
  CheckCircle2,
  Loader2,
  Circle,
} from "lucide-react";

const STEPS = [
  { label: "Uploading document", duration: 1200 },
  { label: "Extracting resume text", duration: 2500 },
  { label: "Identifying resume sections", duration: 4000 },
  { label: "Structuring information with AI", duration: 6000 },
];

export default function ProcessingState({ file }) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const startTime = Date.now();
    const interval = setInterval(() => {
      setElapsed(Date.now() - startTime);
    }, 50);

    return () => clearInterval(interval);
  }, []);

  // Smooth asymptotic progress calculation (approaches 95% while waiting for API response)
  const progressPercent = Math.min(
    95,
    Math.round((1 - Math.exp(-elapsed / 4500)) * 95)
  );

  const isPdf =
    file?.type === "application/pdf" || file?.name?.toLowerCase().endsWith(".pdf");

  return (
    <div className="processing-screen">
      <div className="processing-card">
        {/* Animated Document Icon with Glow Effect */}
        <div className="processing-visual">
          <div className="processing-glow-ring" />
          <div className="processing-glow-ring-outer" />
          <div className="processing-icon-box">
            {isPdf ? <FileText size={32} /> : <FileImage size={32} />}
            <div className="processing-badge-icon">
              <Sparkles size={14} />
            </div>
          </div>
        </div>

        {/* Title and Filename */}
        <h2 className="processing-title">Analyzing your resume</h2>
        <div className="processing-file-badge">
          <span className="file-badge-icon">
            {isPdf ? <FileText size={14} /> : <FileImage size={14} />}
          </span>
          <span className="file-badge-name">
            {file?.name || "Uploaded Resume"}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="progress-section">
          <div className="progress-header">
            <span>Processing Status</span>
            <span className="progress-percent">{progressPercent}%</span>
          </div>
          <div className="progress-bar-track">
            <div
              className="progress-bar-fill"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
        </div>

        {/* Processing Steps List */}
        <div className="processing-steps-list">
          {STEPS.map((step, index) => {
            const isCompleted = elapsed > step.duration;
            const prevDuration = index === 0 ? 0 : STEPS[index - 1].duration;
            const isActive =
              (elapsed >= prevDuration && elapsed <= step.duration) ||
              (index === STEPS.length - 1 && elapsed > step.duration);

            let statusClass = "pending";
            if (isCompleted && index < STEPS.length - 1) statusClass = "completed";
            else if (isActive) statusClass = "active";

            return (
              <div
                key={index}
                className={`processing-step-item ${statusClass}`}
              >
                <div className="step-icon-wrapper">
                  {statusClass === "completed" && (
                    <CheckCircle2 size={16} className="step-icon check" />
                  )}
                  {statusClass === "active" && (
                    <Loader2 size={16} className="step-icon spin active-spin" />
                  )}
                  {statusClass === "pending" && (
                    <Circle size={14} className="step-icon pending" />
                  )}
                </div>

                <span className="step-label">{step.label}</span>

                {statusClass === "active" && (
                  <span className="step-status-tag">In progress...</span>
                )}
                {statusClass === "completed" && (
                  <span className="step-status-tag done">Done</span>
                )}
              </div>
            );
          })}
        </div>

        {/* Informative Note */}
        <p className="processing-subtext">
          {elapsed > 8000
            ? "Connecting to AI backend... (Free-tier server may take a moment to wake up)"
            : "Sending file to FastAPI backend and extracting structured resume data."}
        </p>
      </div>
    </div>
  );
}
