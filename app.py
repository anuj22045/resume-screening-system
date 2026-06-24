import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.preprocess import preprocess_text
from utils.similarity import calculate_similarity
from utils.experience import extract_experience
from utils.skill_extractor import extract_skills

st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def load_css(filepath: str) -> None:
    with open(filepath, encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("style.css")


# Helper utilities
def progress_bar(label: str, value: float, color: str = "blue"):
    pct = min(max(float(value), 0), 100)
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-header">
        <span class="progress-label">{label}</span>
        <span class="progress-value">{pct:.1f}%</span>
        </div>
        <div class="progress-track">
        <div class="progress-fill progress-{color}" style="--w:{pct}%; width:{pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(icon: str, value: str, label: str,
                accent: str = "linear-gradient(90deg,#3b82f6,#8b5cf6)"):
    st.markdown(f"""
    <div class="metric-card" style="--accent:{accent};">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def skill_tags(skills: list, tag_class: str):
    if not skills:
        st.markdown('<p style="color:#475569;font-size:0.88rem;">None found.</p>',
                    unsafe_allow_html=True)
        return
    icon = {"matched": "✅", "missing": "❌", "extracted": "🔷"}.get(tag_class, "•")
    tags_html = "".join(
        f'<span class="skill-tag {tag_class}">{icon} {s.title()}</span>'
        for s in sorted(skills)
    )
    st.markdown(f'<div class="skill-tags-container">{tags_html}</div>',
                unsafe_allow_html=True)


def score_class(score: float) -> str:
    if score >= 70: return "score-high"
    if score >= 45: return "score-medium"
    return "score-low"


def recommendation_banner(skill_pct: float, resume_score: float, missing_skills: list):
    if skill_pct >= 90 and resume_score >= 50 and len(missing_skills) <= 2:
        st.markdown("""
        <div class="rec-banner success">
        <div class="rec-icon">🏆</div>
        <div>
            <div class="rec-title">Excellent Match!</div>
            <div class="rec-body">This resume is highly suitable for the role. Strong alignment across skills and experience.</div>
        </div>
        </div>""", unsafe_allow_html=True)
    elif skill_pct >= 70 and resume_score >= 50 and len(missing_skills) <= 4:
        missing_str = ", ".join(s.title() for s in missing_skills) if missing_skills else "—"
        st.markdown(f"""
        <div class="rec-banner warning">
        <div class="rec-icon">⚡</div>
        <div>
            <div class="rec-title">Good Match – Room to Improve</div>
            <div class="rec-body">Consider strengthening skills in: <strong style="color:#fbbf24;">{missing_str}</strong></div>
        </div>
        </div>""", unsafe_allow_html=True)
    else:
        missing_str = ", ".join(s.title() for s in missing_skills[:6]) if missing_skills else "—"
        st.markdown(f"""
        <div class="rec-banner danger">
        <div class="rec-icon">🎯</div>
        <div>
            <div class="rec-title">Needs Significant Improvement</div>
            <div class="rec-body">Focus on learning: <strong style="color:#f87171;">{missing_str}</strong></div>
        </div>
        </div>""", unsafe_allow_html=True)



#  HERO HEADER

st.markdown("""
<div class="hero-header">
<div class="hero-badge">⚡ AI-Powered · NLP · Instant Analysis</div>
<div class="hero-title">AI Resume Screener</div>
<div class="hero-subtitle">Upload your resume, paste a job description, and get an instant AI-driven match analysis with skill gap insights.</div>
</div>
""", unsafe_allow_html=True)



#  TABS

tab_single, tab_ranking = st.tabs(["📄  Single Resume Analysis", "🏅  Resume Ranking"])


#  TAB 1 – SINGLE RESUME

with tab_single:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📤 Upload Resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your resume here (PDF or DOCX)",
            type=["pdf", "docx"],
            key="single_upload",
            label_visibility="collapsed",
        )
        if uploaded_file:
            st.markdown(
                f'<p style="color:#34d399;font-size:0.85rem;margin-top:8px;">'
                f'✅ <strong>{uploaded_file.name}</strong> uploaded successfully</p>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📋 Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste the job description",
            height=160,
            placeholder="Paste the full job description here…",
            label_visibility="collapsed",
            key="single_jd",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    analyze_btn = st.button("🔍  Analyze Resume", key="analyze_single")

    if analyze_btn:
        if not uploaded_file:
            st.markdown(
                '<div class="rec-banner danger" style="margin-top:16px;"><div class="rec-icon">⚠️</div>'
                '<div><div class="rec-title">No Resume</div>'
                '<div class="rec-body">Please upload a resume to continue.</div></div></div>',
                unsafe_allow_html=True,
            )
        elif not job_description.strip():
            st.markdown(
                '<div class="rec-banner danger" style="margin-top:16px;"><div class="rec-icon">⚠️</div>'
                '<div><div class="rec-title">No Job Description</div>'
                '<div class="rec-body">Please enter a job description.</div></div></div>',
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("🤖 Analysing with NLP…"):
                resume_text      = extract_text_from_pdf(uploaded_file)
                experience       = extract_experience(resume_text)
                clean_resume     = preprocess_text(resume_text)
                clean_jd         = preprocess_text(job_description)

                resume_skills    = sorted(extract_skills(clean_resume))
                jd_skills        = extract_skills(clean_jd)
                matching_skills  = sorted(list(set(resume_skills) & set(jd_skills)))
                missing_skills   = sorted(list(set(jd_skills) - set(resume_skills)))

                skill_match_pct  = round((len(matching_skills) / len(jd_skills)) * 100, 2) \
                                if jd_skills else 0
                similarity_score = calculate_similarity(" ".join(resume_skills), " ".join(jd_skills))
                resume_score     = round(similarity_score * 100, 2)

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

            # ── Metric Cards
            st.markdown('<div class="section-heading">📊 Analysis Dashboard</div>',
                        unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                metric_card("🎯", f"{resume_score}%", "Resume Score",
                            "linear-gradient(90deg,#1d4ed8,#3b82f6)")
            with c2:
                metric_card("🔗", f"{skill_match_pct}%", "Skill Match",
                            "linear-gradient(90deg,#6d28d9,#8b5cf6)")
            with c3:
                exp_val = f"{experience} yr{'s' if experience != 1 else ''}" \
                        if experience > 0 else "N/A"
                metric_card("💼", exp_val, "Experience",
                            "linear-gradient(90deg,#065f46,#10b981)")
            with c4:
                metric_card("⚠️", str(len(missing_skills)), "Missing Skills",
                            "linear-gradient(90deg,#92400e,#f59e0b)")

            # ── Progress Bars
            st.markdown('<div class="glass-card" style="margin-top:8px;">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📈 Score Breakdown</div>',
                        unsafe_allow_html=True)
            pb1, pb2 = st.columns(2)
            with pb1:
                progress_bar("Resume Score",  resume_score,    "blue")
                progress_bar("Skill Match",   skill_match_pct, "purple")
            with pb2:
                jd_cov = min(round((len(jd_skills) / max(len(resume_skills), 1)) * 100, 2), 100)
                match_ratio = min(
                    round((len(matching_skills) / max(len(resume_skills), 1)) * 100, 2), 100
                )
                progress_bar("JD Skill Coverage", jd_cov,      "green")
                progress_bar("Match Ratio",        match_ratio, "orange")
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Skill Tags
            sk1, sk2, sk3 = st.columns(3)
            with sk1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">🔷 Extracted Skills</div>',
                            unsafe_allow_html=True)
                skill_tags(resume_skills, "extracted")
                st.markdown("</div>", unsafe_allow_html=True)
            with sk2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">✅ Matching Skills</div>',
                            unsafe_allow_html=True)
                skill_tags(matching_skills, "matched")
                st.markdown("</div>", unsafe_allow_html=True)
            with sk3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">❌ Missing Skills</div>',
                            unsafe_allow_html=True)
                skill_tags(missing_skills, "missing")
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Recommendation
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">💡 Recommendation</div>',
                        unsafe_allow_html=True)
            recommendation_banner(skill_match_pct, resume_score, missing_skills)
            st.markdown("</div>", unsafe_allow_html=True)

#  TAB 2 – RESUME RANKING

with tab_ranking:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📤 Upload Multiple Resumes</div>',
                unsafe_allow_html=True)
    uploaded_resumes = st.file_uploader(
        "Upload resumes to rank (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="multi_upload",
        label_visibility="collapsed",
    )
    if uploaded_resumes:
        count = len(uploaded_resumes)
        st.markdown(
            f'<p style="color:#34d399;font-size:0.85rem;margin-top:8px;">'
            f'✅ {count} resume{"s" if count > 1 else ""} uploaded</p>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📋 Job Description</div>', unsafe_allow_html=True)
    rank_jd = st.text_area(
        "Paste the job description",
        height=150,
        placeholder="Paste the full job description for ranking…",
        label_visibility="collapsed",
        key="rank_jd",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    rank_btn = st.button("🏅  Rank Resumes", key="rank_btn")

    if rank_btn:
        if not uploaded_resumes:
            st.markdown(
                '<div class="rec-banner danger"><div class="rec-icon">⚠️</div>'
                '<div><div class="rec-title">No Resumes</div>'
                '<div class="rec-body">Please upload at least one resume.</div></div></div>',
                unsafe_allow_html=True,
            )
        elif not rank_jd.strip():
            st.markdown(
                '<div class="rec-banner danger"><div class="rec-icon">⚠️</div>'
                '<div><div class="rec-title">No Job Description</div>'
                '<div class="rec-body">Please enter a job description.</div></div></div>',
                unsafe_allow_html=True,
            )
        else:
            with st.spinner("🤖 Ranking resumes…"):
                clean_jd     = preprocess_text(rank_jd)
                jd_skills    = extract_skills(clean_jd)
                jd_skill_txt = " ".join(jd_skills)

                results = []
                for rf in uploaded_resumes:
                    resume_text     = extract_text_from_pdf(rf)
                    experience      = extract_experience(resume_text)
                    clean_resume    = preprocess_text(resume_text)
                    resume_skills   = sorted(extract_skills(clean_resume))
                    matching        = sorted(list(set(resume_skills) & set(jd_skills)))
                    missing         = sorted(list(set(jd_skills) - set(resume_skills)))
                    skill_match_pct = round((len(matching) / len(jd_skills)) * 100, 2) \
                                    if jd_skills else 0
                    sim_score       = calculate_similarity(" ".join(resume_skills), jd_skill_txt)
                    resume_score    = round(sim_score * 100, 2)
                    # composite: 60% similarity + 40% skill match
                    composite       = round(0.6 * resume_score + 0.4 * skill_match_pct, 2)
                    results.append({
                        "name":          rf.name,
                        "composite":     composite,
                        "resume_score":  resume_score,
                        "skill_match":   skill_match_pct,
                        "experience":    experience,
                        "matching":      matching,
                        "missing":       missing,
                        "resume_skills": resume_skills,
                    })

                results.sort(key=lambda x: x["composite"], reverse=True)

            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

            # ── Summary cards
            st.markdown('<div class="section-heading">🏆 Ranking Results</div>',
                        unsafe_allow_html=True)
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                metric_card("📄", str(len(results)), "Resumes Ranked",
                            "linear-gradient(90deg,#1d4ed8,#3b82f6)")
            with rc2:
                name_short = results[0]["name"]
                name_short = name_short[:20] + "…" if len(name_short) > 20 else name_short
                metric_card("🏆", name_short, "Top Candidate",
                            "linear-gradient(90deg,#92400e,#f59e0b)")
            with rc3:
                metric_card("⭐", f"{results[0]['composite']}%", "Best Score",
                            "linear-gradient(90deg,#065f46,#10b981)")

            # ── Ranking Table
            st.markdown('<div class="glass-card" style="margin-top:16px;">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📊 Detailed Ranking</div>',
                        unsafe_allow_html=True)
            rows_html = ""
            for i, r in enumerate(results):
                rank_num  = i + 1
                badge_cls = {1: "rank-1", 2: "rank-2", 3: "rank-3"}.get(rank_num, "rank-other")
                medal     = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank_num, f"#{rank_num}")
                sc_cls    = score_class(r["composite"])
                exp_str   = f"{r['experience']} yr{'s' if r['experience'] != 1 else ''}" \
                            if r["experience"] > 0 else "N/A"
                rows_html += f"""
                <tr>
                <td><span class="rank-badge {badge_cls}">{medal}</span></td>
                <td style="color:#f1f5f9;font-weight:600;">{r['name']}</td>
                <td><span class="score-pill {sc_cls}">{r['composite']}%</span></td>
                <td style="color:#60a5fa;">{r['resume_score']}%</td>
                <td style="color:#a78bfa;">{r['skill_match']}%</td>
                <td style="color:#34d399;">{exp_str}</td>
                <td style="color:#64748b;">{len(r['matching'])}/{len(jd_skills)}</td>
                </tr>"""

            st.markdown(f"""
            <table class="rank-table">
            <thead>
                <tr>
                <th>Rank</th><th>Resume</th><th>Overall Score</th>
                <th>Resume Score</th><th>Skill Match</th>
                <th>Experience</th><th>Skills Matched</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Score Distribution bars
            st.markdown(
                '<div class="section-heading" style="margin-top:24px;">📈 Score Distribution</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            bar_colors = ["blue", "purple", "green", "orange", "red"]
            for i, r in enumerate(results):
                lbl = {0: "🥇", 1: "🥈", 2: "🥉"}.get(i, f"#{i+1}") + f"  {r['name']}"
                progress_bar(lbl, r["composite"], bar_colors[i % len(bar_colors)])
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Per-resume skill breakdown (expandable)
            st.markdown(
                '<div class="section-heading" style="margin-top:8px;">🔍 Per-Resume Skill Breakdown</div>',
                unsafe_allow_html=True,
            )
            for i, r in enumerate(results):
                medal = {0: "🥇", 1: "🥈", 2: "🥉"}.get(i, f"#{i+1}")
                with st.expander(f"{medal}  {r['name']}  —  {r['composite']}% overall score"):
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.markdown(
                            '<div class="section-heading" style="font-size:0.85rem;">🔷 Extracted Skills</div>',
                            unsafe_allow_html=True,
                        )
                        skill_tags(r["resume_skills"], "extracted")
                    with d2:
                        st.markdown(
                            '<div class="section-heading" style="font-size:0.85rem;">✅ Matching Skills</div>',
                            unsafe_allow_html=True,
                        )
                        skill_tags(r["matching"], "matched")
                    with d3:
                        st.markdown(
                            '<div class="section-heading" style="font-size:0.85rem;">❌ Missing Skills</div>',
                            unsafe_allow_html=True,
                        )
                        skill_tags(r["missing"], "missing") 