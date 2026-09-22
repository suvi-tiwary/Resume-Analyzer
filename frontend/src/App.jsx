import { useState, useEffect } from "react";
import { Sparkles } from "lucide-react";
import UploadBox from "./components/UploadBox";
import ProcessingState from "./components/ProcessingState";
import ResumeResult from "./components/ResumeResult";
import ErrorState from "./components/ErrorState";
import { parseResume, warmBackend } from "./services/api";
import "./App.css";

function App() {
  // Pre-warm the Render backend on first load to avoid cold-start timeouts
  useEffect(() => {
    warmBackend();
  }, []);

  // Core Application State
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [resumeData, setResumeData] = useState(null);
  const [error, setError] = useState(null);
  const [inlineError, setInlineError] = useState(null);

  /**
   * Handles file selection with validation
   */
  const handleFileSelect = (file, validationError) => {
    if (validationError) {
      setInlineError(validationError);
      setSelectedFile(null);
      return;
    }

    setInlineError(null);
    setSelectedFile(file);
  };

  /**
   * Removes selected file
   */
  const handleFileRemove = () => {
    setSelectedFile(null);
    setInlineError(null);
  };

  /**
   * Triggers the resume analysis flow
   */
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setError(null);

    try {
      const data = await parseResume(selectedFile);
      setResumeData(data);
      setIsProcessing(false);
      setIsComplete(true);
    } catch (err) {
      setIsProcessing(false);
      setError(
        err.message ||
          "Something went wrong while processing your file. Please try again."
      );
    }
  };

  /**
   * Resets the entire application back to upload state
   */
  const handleReset = () => {
    setSelectedFile(null);
    setIsProcessing(false);
    setIsComplete(false);
    setResumeData(null);
    setError(null);
    setInlineError(null);
  };

  /**
   * Resets from error state back to upload state
   */
  const handleRetry = () => {
    setError(null);
    setIsProcessing(false);
    setIsComplete(false);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <button
          className="brand"
          onClick={handleReset}
          title="Go to Home"
          type="button"
        >
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>

          <div>
            <h2>Resume Analyzer</h2>
            <span>AI-powered resume parsing</span>
          </div>
        </button>

        <div className="header-status">
          <span className="status-dot"></span>
          No login required
        </div>
      </header>

      {/* Main Content Area with State Flow */}
      <main className="main">
        {/* State 1: Processing */}
        {isProcessing && <ProcessingState file={selectedFile} />}

        {/* State 2: Analysis Complete (Result Dashboard) */}
        {!isProcessing && isComplete && resumeData && (
          <ResumeResult resumeData={resumeData} onReset={handleReset} />
        )}

        {/* State 3: Error State */}
        {!isProcessing && error && (
          <ErrorState error={error} onRetry={handleRetry} />
        )}

        {/* State 4: Default Upload State */}
        {!isProcessing && !isComplete && !error && (
          <UploadBox
            file={selectedFile}
            onFileSelect={handleFileSelect}
            onFileRemove={handleFileRemove}
            onAnalyze={handleAnalyze}
            inlineError={inlineError}
            onClearError={() => setInlineError(null)}
          />
        )}
      </main>

      {/* Footer */}
      <footer>
        Resume Analyzer · Built for resume parsing assessment
      </footer>
    </div>
  );
}

export default App;