import { useState } from "react";
import {
  Upload,
  FileText,
  FileImage,
  Sparkles,
  ShieldCheck,
  Zap,
  AlertCircle,
  X,
} from "lucide-react";

export default function UploadBox({
  file,
  onFileSelect,
  onFileRemove,
  onAnalyze,
  inlineError,
  onClearError,
}) {
  const [isDragging, setIsDragging] = useState(false);

  const validateAndHandle = (selectedFile) => {
    if (!selectedFile) return;

    const allowedMimeTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
    ];

    const fileName = selectedFile.name?.toLowerCase() || "";
    const hasValidExtension =
      fileName.endsWith(".pdf") ||
      fileName.endsWith(".jpg") ||
      fileName.endsWith(".jpeg") ||
      fileName.endsWith(".png");

    if (!allowedMimeTypes.includes(selectedFile.type) && !hasValidExtension) {
      onFileSelect(null, "Unsupported file type. Please upload a PDF, JPG or PNG.");
      return;
    }

    onFileSelect(selectedFile, null);
  };

  const handleInputChange = (event) => {
    const selectedFile = event.target.files?.[0];
    validateAndHandle(selectedFile);
    // Reset target value so selecting the same file again still fires change
    event.target.value = "";
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    const droppedFile = event.dataTransfer.files?.[0];
    validateAndHandle(droppedFile);
  };

  return (
    <div className="upload-container">
      {/* Hero Section */}
      <section className="hero">
        <div className="badge">
          <Sparkles size={15} />
          Smart Resume Parser
        </div>

        <h1>
          Turn your resume into
          <span> structured data.</span>
        </h1>

        <p>
          Upload your resume and let our parser extract your personal details,
          skills, education, and work experience.
        </p>
      </section>

      {/* Upload Card */}
      <section className="upload-section">
        {/* Inline Error Banner */}
        {inlineError && (
          <div className="inline-error-banner" role="alert">
            <div className="inline-error-content">
              <AlertCircle size={18} />
              <span>{inlineError}</span>
            </div>
            {onClearError && (
              <button
                type="button"
                className="inline-error-close"
                onClick={onClearError}
                aria-label="Dismiss error"
              >
                <X size={15} />
              </button>
            )}
          </div>
        )}

        <div
          className={`upload-box ${isDragging ? "dragging" : ""}`}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          {!file ? (
            <>
              <div className="upload-icon">
                <Upload size={30} />
              </div>

              <h3>Drop your resume here</h3>

              <p>or click the button below to browse your files</p>

              <label className="upload-button">
                <Upload size={18} />
                Choose Resume
                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={handleInputChange}
                  hidden
                />
              </label>

              <div className="file-types">
                <span>
                  <FileText size={15} />
                  PDF
                </span>

                <span>
                  <FileImage size={15} />
                  JPG
                </span>

                <span>
                  <FileImage size={15} />
                  PNG
                </span>
              </div>
            </>
          ) : (
            <div className="selected-file">
              <div className="selected-file-icon">
                {file.type === "application/pdf" ||
                file.name.toLowerCase().endsWith(".pdf") ? (
                  <FileText size={28} />
                ) : (
                  <FileImage size={28} />
                )}
              </div>

              <div className="file-info">
                <h3>{file.name}</h3>
                <p>{(file.size / 1024).toFixed(1)} KB</p>
              </div>

              <button
                type="button"
                className="remove-button"
                onClick={onFileRemove}
                title="Remove file"
                aria-label="Remove selected file"
              >
                <X size={18} />
              </button>
            </div>
          )}
        </div>

        {file && (
          <button
            type="button"
            className="analyze-button"
            onClick={onAnalyze}
            aria-label="Analyze Resume"
          >
            <Sparkles size={18} />
            Analyze Resume
          </button>
        )}
      </section>

      {/* Features */}
      <section className="features">
        <div className="feature-card">
          <div className="feature-icon">
            <Zap size={20} />
          </div>

          <div>
            <h4>Fast Processing</h4>
            <p>Extract resume information quickly.</p>
          </div>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <ShieldCheck size={20} />
          </div>

          <div>
            <h4>Simple & Private</h4>
            <p>No account or login required.</p>
          </div>
        </div>

        <div className="feature-card">
          <div className="feature-icon">
            <FileText size={20} />
          </div>

          <div>
            <h4>Structured Output</h4>
            <p>Get clean and consistent JSON.</p>
          </div>
        </div>
      </section>

      {/* Supported Files Notice */}
      <div className="notice">
        <AlertCircle size={17} />
        <span>Supported formats: PDF, JPG and PNG</span>
      </div>
    </div>
  );
}
