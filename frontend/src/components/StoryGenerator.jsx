import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import { API_BASE_URL } from "../util.js";

function StoryGenerator() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState(""); // Store the actual theme

  const handleThemeSubmit = async (submittedTheme) => {
    setLoading(true);
    setError(null);
    setTheme(submittedTheme); // Save the theme

    try {
      // Step 1: Create the story job
      const createResponse = await axios.post(
        `${API_BASE_URL}/stories/create`,
        { theme: submittedTheme },
      );

      const jobId = createResponse.data.job_id;
      console.log("Job created:", jobId);

      // Step 2: Poll for job completion
      const storyId = await pollJobStatus(jobId);

      // Step 3: Navigate to the story
      navigate(`/story/${storyId}`);
    } catch (err) {
      console.error("Error creating story:", err);
      setError(err.response?.data?.detail || "Failed to create story");
      setLoading(false);
    }
  };

  const pollJobStatus = async (jobId) => {
    return new Promise((resolve, reject) => {
      const maxAttempts = 60; // 60 seconds max
      let attempts = 0;

      const checkStatus = async () => {
        try {
          attempts++;

          const response = await axios.get(
            `${API_BASE_URL}/stories/jobs/${jobId}`,
          );

          const job = response.data;
          console.log(`Polling attempt ${attempts}:`, job.status);

          if (job.status === "completed") {
            console.log("Story completed! ID:", job.story_id);
            resolve(job.story_id);
          } else if (job.status === "failed") {
            reject(new Error(job.error || "Story generation failed"));
          } else if (attempts >= maxAttempts) {
            reject(new Error("Story generation timed out"));
          } else {
            // Still processing, check again in 1 second
            setTimeout(checkStatus, 1000);
          }
        } catch (err) {
          reject(err);
        }
      };

      // Start polling
      checkStatus();
    });
  };

  if (loading) {
    return <LoadingStatus theme={theme} />;
  }

  if (error) {
    return (
      <div className="story-generator">
        <div className="error-message">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={() => setError(null)}>Try Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="story-generator">
      <ThemeInput onSubmit={handleThemeSubmit} />
    </div>
  );
}

export default StoryGenerator;
