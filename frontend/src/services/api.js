import axios from "axios";

// AWS EC2 backend (HTTPS via Nginx + Let's Encrypt)
const DEFAULT_API_BASE = "https://3.110.90.31";
const API_BASE = import.meta.env.VITE_API_URL || DEFAULT_API_BASE;

/**
 * Silently pings the backend to wake it from Render's free-tier idle sleep.
 * Call this on app load so the backend is warm by the time the user uploads.
 */
export async function warmBackend() {
  try {
    console.log("[API] Warming backend:", `${API_BASE}/health`);
    await axios.get(`${API_BASE}/health`, { timeout: 60000 });
    console.log("[API] Backend is warm and ready.");
  } catch {
    // Silently ignore — this is a best-effort warm-up ping
    console.warn("[API] Backend warm-up ping failed (may still be starting).");
  }
}

/**
 * Sends a resume file to the deployed FastAPI backend for parsing.
 *
 * @param {File} file - Resume file (PDF, JPG, JPEG, PNG)
 * @returns {Promise<Object>} Parsed resume JSON data
 */
export async function parseResume(file) {
  if (!file) {
    throw new Error("Please select a resume file to analyze.");
  }

  const formData = new FormData();
  formData.append("file", file);

  const endpoint = `${API_BASE}/api/resume/parse`;
  console.log("[API] Request started → POST", endpoint);
  console.log(
    "[API] File:",
    file.name,
    `(${(file.size / 1024).toFixed(1)} KB)`,
    file.type
  );

  try {
    // IMPORTANT: Do NOT set Content-Type manually with FormData.
    // Let Axios set it automatically with the correct multipart boundary.
    const response = await axios.post(endpoint, formData, {
      timeout: 90000, // 90s for free-tier Render cold start
    });

    console.log("[API] Response status:", response.status);
    console.log("[API] Response data:", response.data);

    const data = response.data;

    // Normalize response to handle nulls or schema variations safely
    const normalizedData = {
      name: data?.name || "",
      email: data?.email || "",
      phone: data?.phone || "",
      skills: Array.isArray(data?.skills) ? data.skills : [],
      education: Array.isArray(data?.education)
        ? data.education.map((item) => ({
            degree: item?.degree || "",
            institution:
              item?.institution || item?.school || item?.college || "",
            field: item?.field || "",
            start_year: item?.start_year ? String(item.start_year) : "",
            end_year: item?.end_year ? String(item.end_year) : "",
          }))
        : [],
      work_experience: Array.isArray(data?.work_experience)
        ? data.work_experience.map((item) => ({
            job_title: item?.job_title || item?.position || item?.title || "",
            company: item?.company || "",
            start_date: item?.start_date || "",
            end_date:
              item?.end_date || (item?.years ? `${item.years} years` : ""),
            description: item?.description || "",
          }))
        : [],
      ...data,
    };

    return normalizedData;
  } catch (error) {
    if (error.response) {
      // Server responded with a 4xx/5xx error
      console.error(
        "[API] Server error:",
        error.response.status,
        error.response.data
      );

      const errDetail =
        error.response.data?.detail || error.response.data?.message;

      if (typeof errDetail === "string") {
        throw new Error(errDetail);
      } else if (Array.isArray(errDetail)) {
        const messages = errDetail.map((e) => e.msg || JSON.stringify(e));
        throw new Error(messages.join(", "));
      } else if (error.response.status === 422) {
        throw new Error(
          "Invalid file. Please upload a PDF, JPG, or PNG resume."
        );
      } else if (error.response.status === 400) {
        throw new Error(
          "Could not read text from this file. Please try a different resume."
        );
      } else if (error.response.status >= 500) {
        throw new Error("The server encountered an error. Please try again.");
      } else {
        throw new Error(
          `Server error (${error.response.status}): Unable to parse resume.`
        );
      }
    } else if (error.code === "ECONNABORTED") {
      console.error(
        "[API] Request timed out after",
        error.config?.timeout,
        "ms"
      );
      throw new Error(
        "Request timed out. The backend server might be starting up from idle—please wait a moment and try again."
      );
    } else {
      // Network Error or CORS block — no response received at all
      console.error("[API] Network/CORS error:", error.message);
      throw new Error(
        "Unable to reach the backend server. This may be a network or CORS issue—please try again."
      );
    }
  }
}
