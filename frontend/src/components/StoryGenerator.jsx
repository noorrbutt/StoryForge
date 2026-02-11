import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import { API_BASE_URL } from "../util.js";

function StoryGenerator() {
  const navigate = useNavigate();
  const [theme, setTheme] = useState("");
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStory = useCallback(
    (id) => {
      setLoading(false);
      setJobStatus("completed");
      navigate(`/story/${id}`);
    },
    [navigate],
  );

  const pollJobStatus = useCallback(
    async (id) => {
      try {
        const response = await axios.get(`${API_BASE_URL}/jobs/${id}`);
        const { status, story_id, error: jobError } = response.data;
        setJobStatus(status);

        if (status === "completed" && story_id) {
          fetchStory(story_id);
        } else if (status === "failed" || jobError) {
          setError(jobError || "Failed to generate story");
          setLoading(false);
        }
      } catch (e) {
        if (e.response?.status !== 404) {
          setError(`Failed to check story status: ${e.message}`);
          setLoading(false);
        }
      }
    },
    [fetchStory],
  );

  useEffect(() => {
    if (!jobId || jobStatus !== "processing") return;

    const pollInterval = setInterval(() => {
      pollJobStatus(jobId);
    }, 5000);

    return () => clearInterval(pollInterval);
  }, [jobId, jobStatus, pollJobStatus]);

  const generateStory = async (theme) => {
    setLoading(true);
    setError(null);
    setTheme(theme);

    try {
      const response = await axios.post(`${API_BASE_URL}/stories/create`, {
        theme,
      });
      const { job_id, status } = response.data;
      setJobId(job_id);
      setJobStatus(status);
    } catch (e) {
      setLoading(false);
      setError(`Failed to generate story: ${e.message}`);
    }
  };

  const reset = () => {
    setJobId(null);
    setJobStatus(null);
    setError(null);
    setTheme("");
    setLoading(false);
  };

  return (
    <div className="story-generator">
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}

      {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory} />}

      {loading && <LoadingStatus theme={theme} />}
    </div>
  );
}

export default StoryGenerator;
