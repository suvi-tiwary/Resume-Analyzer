import { useState } from "react";
import { Code, Copy, Check } from "lucide-react";

export default function JsonViewer({ data }) {
  const [copied, setCopied] = useState(false);

  const jsonString = JSON.stringify(data, null, 2);

  const handleCopy = async () => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(jsonString);
      } else {
        // Fallback for non-https or older environments
        const textArea = document.createElement("textarea");
        textArea.value = jsonString;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand("copy");
        textArea.remove();
      }
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy JSON:", err);
    }
  };

  /**
   * Simple helper to syntax-highlight formatted JSON string for rich editor look.
   */
  const highlightJson = (json) => {
    if (!json) return "";
    return json.replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?)/g,
      (match) => {
        let cls = "json-number";
        if (/^"/.test(match)) {
          if (/:$/.test(match)) {
            cls = "json-key";
          } else {
            cls = "json-string";
          }
        } else if (/true|false/.test(match)) {
          cls = "json-boolean";
        } else if (/null/.test(match)) {
          cls = "json-null";
        }
        return `<span class="${cls}">${match}</span>`;
      }
    );
  };

  return (
    <div className="json-viewer-container">
      <div className="json-viewer-header">
        <div className="json-header-left">
          <div className="json-header-icon">
            <Code size={16} />
          </div>
          <div>
            <h4>Raw Extracted JSON</h4>
            <span>application/json</span>
          </div>
        </div>

        <button
          className={`copy-json-button ${copied ? "copied" : ""}`}
          onClick={handleCopy}
          type="button"
          aria-label="Copy JSON to clipboard"
        >
          {copied ? (
            <>
              <Check size={14} />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Copy size={14} />
              <span>Copy JSON</span>
            </>
          )}
        </button>
      </div>

      <div className="json-viewer-body">
        <pre className="json-pre">
          <code
            dangerouslySetInnerHTML={{
              __html: highlightJson(jsonString),
            }}
          />
        </pre>
      </div>
    </div>
  );
}
