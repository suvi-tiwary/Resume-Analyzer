import { ArrowLeft, CheckCircle2 } from "lucide-react";
import PersonalInfo from "./PersonalInfo";
import Skills from "./Skills";
import Education from "./Education";
import Experience from "./Experience";
import JsonViewer from "./JsonViewer";

export default function ResumeResult({ resumeData, onReset }) {
  if (!resumeData) return null;

  return (
    <div className="resume-result-screen">
      {/* Result Screen Header */}
      <div className="result-top-bar">
        <div className="result-title-group">
          <div className="result-badge">
            <CheckCircle2 size={14} />
            <span>Analysis Complete</span>
          </div>
          <h2>Resume Analysis</h2>
          <p>Information extracted from your resume</p>
        </div>

        <button
          className="reset-button"
          onClick={onReset}
          type="button"
          aria-label="Analyze another resume"
        >
          <ArrowLeft size={16} />
          <span>Analyze Another Resume</span>
        </button>
      </div>

      {/* Two Column Result Layout */}
      <div className="result-dashboard-grid">
        {/* Left Column: Structured Readable Resume */}
        <div className="result-readable-column">
          <PersonalInfo data={resumeData} />
          <Skills skills={resumeData.skills} />
          <Experience experiences={resumeData.work_experience} />
          <Education education={resumeData.education} />
        </div>

        {/* Right Column: Raw JSON Panel */}
        <div className="result-json-column">
          <JsonViewer data={resumeData} />
        </div>
      </div>
    </div>
  );
}
