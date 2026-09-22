import { Sparkles } from "lucide-react";

export default function Skills({ skills }) {
  const validSkills = Array.isArray(skills) ? skills.filter(Boolean) : [];

  return (
    <div className="result-card skills-card">
      <div className="card-header">
        <div className="card-header-icon">
          <Sparkles size={18} />
        </div>
        <h3>Skills</h3>
        <span className="skills-count-badge">{validSkills.length}</span>
      </div>

      {validSkills.length > 0 ? (
        <div className="skills-grid">
          {validSkills.map((skill, index) => (
            <span key={index} className="skill-pill">
              {typeof skill === "object" ? JSON.stringify(skill) : String(skill)}
            </span>
          ))}
        </div>
      ) : (
        <p className="empty-section-text">
          No specific technical skills were identified in this resume.
        </p>
      )}
    </div>
  );
}
