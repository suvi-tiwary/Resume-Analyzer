import { Briefcase, Calendar, Building } from "lucide-react";

export default function Experience({ experiences }) {
  const list = Array.isArray(experiences) ? experiences : [];

  return (
    <div className="result-card experience-card">
      <div className="card-header">
        <div className="card-header-icon">
          <Briefcase size={18} />
        </div>
        <h3>Work Experience</h3>
        {list.length > 0 && (
          <span className="skills-count-badge">{list.length}</span>
        )}
      </div>

      {list.length > 0 ? (
        <div className="timeline-list">
          {list.map((exp, index) => {
            const title =
              exp?.job_title || exp?.position || exp?.title || "Role / Position";
            const company = exp?.company || "";
            const duration =
              exp?.start_date && exp?.end_date
                ? `${exp.start_date} — ${exp.end_date}`
                : exp?.start_date ||
                  exp?.end_date ||
                  (exp?.years ? `${exp.years} years` : "");
            const description = exp?.description || "";

            return (
              <div key={index} className="timeline-item">
                <div className="timeline-marker">
                  <div className="timeline-dot" />
                  {index < list.length - 1 && <div className="timeline-line" />}
                </div>

                <div className="timeline-content">
                  <div className="timeline-header-row">
                    <div>
                      <h4 className="job-title">{title}</h4>
                      {company && (
                        <p className="company-name">
                          <Building size={14} />
                          <span>{company}</span>
                        </p>
                      )}
                    </div>

                    {duration && (
                      <span className="timeline-badge">
                        <Calendar size={13} />
                        {duration}
                      </span>
                    )}
                  </div>

                  {description && (
                    <p className="experience-description">{description}</p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="empty-section-text">
          No work experience records identified in this document.
        </p>
      )}
    </div>
  );
}
