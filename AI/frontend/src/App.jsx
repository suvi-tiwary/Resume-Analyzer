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
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      alert("Please upload a PDF, JPG, or PNG file.");
      return;
    }

    setFile(selectedFile);
  };

  const handleInputChange = (event) => {
    const selectedFile = event.target.files?.[0];
    handleFile(selectedFile);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    const droppedFile = event.dataTransfer.files?.[0];
    handleFile(droppedFile);
  };

  const removeFile = () => {
    setFile(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="brand">
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>

          <div>
            <h2>Resume Analyzer</h2>
            <span>AI-powered resume parsing</span>
          </div>
        </div>

        <div className="header-status">
          <span className="status-dot"></span>
          No login required
        </div>
      </header>

      {/* Main */}
      <main className="main">
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
            Upload your resume and let our parser extract your
            personal details, skills, education, and work experience.
          </p>
        </section>

        {/* Upload Card */}
        <section className="upload-section">
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

                <p>
                  or click the button below to browse your files
                </p>

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
                  {file.type === "application/pdf" ? (
                    <FileText size={28} />
                  ) : (
                    <FileImage size={28} />
                  )}
                </div>

                <div className="file-info">
                  <h3>{file.name}</h3>

                  <p>
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>

                <button
                  className="remove-button"
                  onClick={removeFile}
                  title="Remove file"
                >
                  <X size={18} />
                </button>
              </div>
            )}
          </div>

          {file && (
            <button className="analyze-button">
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
              <p>
                Extract resume information quickly.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <ShieldCheck size={20} />
            </div>

            <div>
              <h4>Simple & Private</h4>
              <p>
                No account or login required.
              </p>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">
              <FileText size={20} />
            </div>

            <div>
              <h4>Structured Output</h4>
              <p>
                Get clean and consistent JSON.
              </p>
            </div>
          </div>
        </section>

        {/* Supported Files */}
        <div className="notice">
          <AlertCircle size={17} />
          <span>
            Supported formats: PDF, JPG and PNG
          </span>
        </div>
      </main>

      <footer>
        Resume Analyzer · Built for resume parsing assessment
      </footer>
    </div>
  );
}

export default App;