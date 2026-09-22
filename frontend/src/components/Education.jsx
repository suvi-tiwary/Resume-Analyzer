import { GraduationCap, Calendar, Building2 } from "lucide-react";

export default function Education({ education }) {
  const list = Array.isArray(education) ? education : [];

  return (
    <div className="result-card education-card">
      <div className="card-header">
        <div className="card-header-icon">
          <GraduationCap size={18} />
        </div>
        <h3>Education</h3>
        {list.length > 0 && (
          <span className="skills-count-badge">{list.length}</span>
        )}
      </div>

      {list.length > 0 ? (
        <div className="timeline-list">
          {list.map((item, index) => {
            const degree = item?.degree || "Degree";
            const field = item?.field || "";
            const institution =
              item?.institution || item?.school || item?.collge || "";
            const years =
              item?.start_year && item?.end_year
                ? `${item.start_year} — ${item.end_year}`
                : item?.start_year || item?.end_year || "";

            return (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">
                  <div className="timeline-dot" />
                  {index < list.length - 1 && <div className="timeline-line" />}
                </div>

                <div className="timeline-content">
                  <div className="timeline-header-row">
                    <div>
                      <h4 className="degree-title">
                        {degree}
                        {field && (
                          <span className="field-separator"> in {field}</span>
                        )}
                      </h4>

                      {institution && (
                        <p className="institution-name">
                          <Building2 size={14} />
                          <span>{institution}</span>
                        </p>
                      )}
                    </div>

                    {years && (
                      <span className="timeline-badge">
                        <Calendar size={13} />
                        {years}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="empty-section-text">
          No education history identified in this document.
        </p>
      )}
    </div>
  );
}
