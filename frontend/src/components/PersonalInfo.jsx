import { User, Mail, Phone } from "lucide-react";

export default function PersonalInfo({ data }) {
  const name = data?.name || "Candidate Name Not Detected";
  const email = data?.email || "";
  const phone = data?.phone || "";

  return (
    <div className="result-card personal-info-card">
      <div className="card-header">
        <div className="card-header-icon">
          <User size={18} />
        </div>
        <h3>Personal Information</h3>
      </div>

      <div className="personal-info-body">
        <h2 className="personal-name">{name}</h2>

        <div className="personal-details-grid">
          {email ? (
            <div className="personal-detail-item">
              <span className="detail-icon">
                <Mail size={15} />
              </span>
              <a href={`mailto:${email}`} className="detail-value link-value">
                {email}
              </a>
            </div>
          ) : null}

          {phone ? (
            <div className="personal-detail-item">
              <span className="detail-icon">
                <Phone size={15} />
              </span>
              <a href={`tel:${phone}`} className="detail-value link-value">
                {phone}
              </a>
            </div>
          ) : null}

          {!email && !phone && (
            <p className="empty-section-text">
              No contact details (email or phone) detected.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
