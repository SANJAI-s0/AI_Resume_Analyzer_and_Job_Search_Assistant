const uploadArea = document.getElementById("upload-area");
const uploadText = document.getElementById("upload-text");
const fileInput = document.getElementById("resume-file");
const analyzeBtn = document.getElementById("analyze-btn");
const loading = document.getElementById("loading");
const formSection = document.getElementById("form-section");
const results = document.getElementById("results");
const analysisGrid = document.getElementById("analysis-grid");
const jobsGrid = document.getElementById("jobs-grid");
const resetBtn = document.getElementById("reset-btn");

/* =========================
   Upload (Click)
========================= */
uploadArea.addEventListener("click", () => fileInput.click());

/* =========================
   File Select
========================= */
fileInput.addEventListener("change", () => {
    if (!fileInput.files.length) return;

    const file = fileInput.files[0];
    if (file.type !== "application/pdf") {
        alert("Please upload a PDF file only.");
        return;
    }

    uploadText.innerHTML = `✅ ${file.name}`;
    analyzeBtn.disabled = false;
});

/* =========================
   Drag & Drop
========================= */
["dragenter", "dragover"].forEach(event => {
    uploadArea.addEventListener(event, e => {
        e.preventDefault();
        uploadArea.classList.add("dragover");
    });
});

["dragleave", "drop"].forEach(event => {
    uploadArea.addEventListener(event, e => {
        e.preventDefault();
        uploadArea.classList.remove("dragover");
    });
});

uploadArea.addEventListener("drop", e => {
    const file = e.dataTransfer.files[0];
    if (!file || file.type !== "application/pdf") {
        alert("Only PDF files are supported.");
        return;
    }

    fileInput.files = e.dataTransfer.files;
    uploadText.innerHTML = `✅ ${file.name}`;
    analyzeBtn.disabled = false;
});

/* =========================
   Analyze Resume
========================= */
analyzeBtn.addEventListener("click", async () => {
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append("resume", fileInput.files[0]);
    formData.append("desired_role", document.getElementById("desired-role").value);
    formData.append("city", document.getElementById("city").value);
    formData.append("country", document.getElementById("country").value);

    if (document.getElementById("remote-only").checked) {
        formData.append("remote_only", "on");
    }

    formSection.style.display = "none";
    loading.style.display = "block";

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            throw new Error("Analysis failed");
        }

        const data = await res.json();
        renderResults(data);

    } catch (err) {
        alert("Resume analysis failed. Please try again.");
        console.error(err);
        window.location.reload();
    } finally {
        loading.style.display = "none";
    }
});

/* =========================
   Render Results
========================= */
function renderResults(data) {
    results.style.display = "block";

    /* Analysis */
    analysisGrid.innerHTML = `
        <div class="analysis-card">
            <div class="role-badge">💯 Score: ${data.resume_score ?? 0}%</div>
            <h3>${data.analysis?.role || "Professional"}</h3>
            <p>${data.analysis?.summary || "Profile analyzed successfully."}</p>
        </div>
        <div class="analysis-card">
            <h3>Skills</h3>
            <div class="skills-tags">
                ${(data.analysis?.skills || [])
                    .map(skill => `<span class="skill-tag">${skill}</span>`)
                    .join("") || "<span>No skills detected</span>"}
            </div>
        </div>
    `;

    /* Jobs */
    if (!data.jobs || data.jobs.length === 0) {
        jobsGrid.innerHTML = `
            <div class="job-card">
                <p>No jobs found for your profile.</p>
                <p>Try a different role or city.</p>
            </div>
        `;
        return;
    }

    jobsGrid.innerHTML = data.jobs.map(job => `
        <div class="job-card">
            <h3>${job.title || "Job Role"}</h3>
            <p>${job.company || "Company"} • ${job.location || ""}</p>

            ${
                job.url && job.url.startsWith("http")
                    ? `<a class="job-link" href="${job.url}" target="_blank" rel="noopener noreferrer">View Job</a>`
                    : `<span style="opacity:.6">Job link unavailable</span>`
            }
        </div>
    `).join("");
}

/* =========================
   Reset
========================= */
resetBtn.addEventListener("click", () => {
    window.location.reload();
});
