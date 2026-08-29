import json
import logging

from sqlalchemy.orm import Session

from app.config import settings
from app.models.job_listing import JobListing
from app.utils.exceptions import ValidationError, ServiceUnavailableError

logger = logging.getLogger(__name__)


class MatchingService:
    def __init__(self, db: Session):
        self.db = db

    def match(self, query: str) -> dict:
        # Validate query
        if not query or not query.strip():
            raise ValidationError("Please provide a non-empty description of what you're looking for")

        if len(query) > 1000:
            raise ValidationError("Query exceeds the maximum allowed length of 1000 characters")

        # Fetch all open jobs
        jobs = self.db.query(JobListing).filter(JobListing.status == "open").all()

        if not jobs:
            return {"results": [], "message": "No open job listings found"}

        # Call AI matching
        try:
            results = self._call_ai_matching(query, jobs)
        except Exception as e:
            logger.error(f"Matching service error: {e}")
            raise ServiceUnavailableError("Matching Engine")

        if not results:
            return {"results": [], "message": "No matches found for your query"}

        return {"results": results[:20], "message": None}

    def _call_ai_matching(self, query: str, jobs: list) -> list:
        """Call OpenAI API for job matching."""
        if not settings.OPENAI_API_KEY:
            # Fallback: simple keyword matching when no API key
            return self._keyword_matching(query, jobs)

        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            prompt = self._build_prompt(query, jobs)

            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a job matching assistant. Return only valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                timeout=30,
            )

            content = response.choices[0].message.content
            return self._parse_response(content, jobs)

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to keyword matching
            return self._keyword_matching(query, jobs)

    def _build_prompt(self, query: str, jobs: list) -> str:
        job_summaries = []
        for job in jobs:
            skills = ", ".join(job.required_skills) if job.required_skills else "None"
            job_summaries.append(
                f"Job ID: {job.id} | Title: {job.title} | "
                f"Skills: {skills} | Level: {job.experience_level} | "
                f"Location: {job.location}"
            )

        jobs_text = "\n".join(job_summaries)

        return f"""Given a candidate's description of their ideal role and a list of job openings,
score each job from 0-100 on how well it matches the candidate's preferences.
Provide a brief explanation for each match.

Candidate's description: {query}

Available jobs:
{jobs_text}

Respond in JSON format as an array:
[{{"job_id": <int>, "score": <int 0-100>, "explanation": "<brief reason>"}}]

Only include jobs with score > 20. Sort by score descending."""

    def _parse_response(self, content: str, jobs: list) -> list:
        """Parse AI response into structured results."""
        try:
            # Clean response - sometimes wrapped in markdown code blocks
            content = content.strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0]

            data = json.loads(content)
            job_map = {j.id: j for j in jobs}

            results = []
            for item in data:
                job_id = item.get("job_id")
                if job_id not in job_map:
                    continue
                score = max(0, min(100, int(item.get("score", 0))))
                explanation = item.get("explanation", "Match based on relevance")
                results.append({
                    "job_id": job_id,
                    "title": job_map[job_id].title,
                    "score": score,
                    "explanation": explanation,
                })

            results.sort(key=lambda x: -x["score"])
            return results[:20]

        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise ServiceUnavailableError("Matching Engine")

    def _keyword_matching(self, query: str, jobs: list) -> list:
        """Simple keyword-based matching fallback when OpenAI is unavailable."""
        query_words = set(query.lower().split())
        results = []

        for job in jobs:
            score = 0
            matches = []

            # Match against title
            title_words = set(job.title.lower().split())
            title_overlap = query_words & title_words
            if title_overlap:
                score += len(title_overlap) * 15
                matches.append(f"Title contains: {', '.join(title_overlap)}")

            # Match against skills
            if job.required_skills:
                for skill in job.required_skills:
                    if skill.lower() in query.lower():
                        score += 20
                        matches.append(f"Matching skill: {skill}")

            # Match against location
            if job.location and job.location.lower() in query.lower():
                score += 15
                matches.append(f"Location match: {job.location}")

            # Match against experience level
            if job.experience_level and job.experience_level.lower() in query.lower():
                score += 10
                matches.append(f"Experience level match: {job.experience_level}")

            # Match against description keywords
            desc_words = set(job.description.lower().split())
            desc_overlap = query_words & desc_words
            if desc_overlap:
                score += len(desc_overlap) * 5
                matches.append(f"Description relevance: {len(desc_overlap)} keyword matches")

            score = min(100, score)
            if score > 10:
                explanation = "; ".join(matches) if matches else "Partial keyword match"
                results.append({
                    "job_id": job.id,
                    "title": job.title,
                    "score": score,
                    "explanation": explanation,
                })

        results.sort(key=lambda x: -x["score"])
        return results[:20]
