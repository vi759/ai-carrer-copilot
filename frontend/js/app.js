async function analyzeResume() {

    const resumeFile =
        document.getElementById("resume").files[0];

    const jobDescription =
        document.getElementById("jobDescription").value;

    if (!resumeFile) {
        alert("Please upload a resume PDF");
        return;
    }

    if (!jobDescription.trim()) {
        alert("Please enter a Job Description");
        return;
    }

    const formData = new FormData();

    formData.append(
        "resume",
        resumeFile
    );

    formData.append(
        "job_description",
        jobDescription
    );

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        console.log(data);

        document.getElementById("results").style.display =
            "block";

        document.getElementById("atsScore").innerText =
            data.ats_score + "%";

        document.getElementById("skillMatch").innerText =
            data.skill_match_percentage + "%";

        const skillsList =
            document.getElementById("missingSkills");

        skillsList.innerHTML = "";

        data.missing_skills.forEach(skill => {

            const li =
                document.createElement("li");

            li.textContent = skill;

            skillsList.appendChild(li);

        });

    } catch (error) {

        console.error(error);

        alert(
            "Failed to connect to backend"
        );

    }

}