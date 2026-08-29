"""Seed script to populate database with sample data for development."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.job_listing import JobListing
from app.models.candidate_profile import CandidateProfile
from app.utils.auth import hash_password


# A broad set of sample jobs spanning many locations, skills, and all levels.
JOBS = [
    ("Senior Python Backend Engineer",
     "Build scalable backend systems for our healthcare platform using FastAPI, PostgreSQL, and AWS.",
     ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker"], "Senior", "Remote"),
    ("Full Stack Developer - React & Node.js",
     "Build modern web applications for our fintech products, working across frontend and backend.",
     ["React", "Node.js", "TypeScript", "MongoDB", "REST APIs"], "Mid", "Bengaluru, India"),
    ("Junior Data Analyst",
     "Analyze customer data, build dashboards, and support decisions with insights.",
     ["Python", "SQL", "Tableau", "Statistics"], "Entry", "Hyderabad, India"),
    ("Machine Learning Engineer",
     "Build and deploy ML models and NLP systems for our recommendation engine.",
     ["Python", "TensorFlow", "PyTorch", "NLP", "MLOps"], "Senior", "Remote"),
    ("DevOps Engineer",
     "Manage cloud infrastructure and CI/CD pipelines for high-availability systems.",
     ["AWS", "Kubernetes", "Terraform", "Docker", "CI/CD"], "Mid", "Pune, India"),
    ("Lead Software Architect",
     "Define system architecture and lead engineering teams on large-scale distributed systems.",
     ["System Design", "Microservices", "Java", "Kafka", "Leadership"], "Lead", "Mumbai, India"),
    ("Frontend Engineer - Angular",
     "Craft responsive, accessible UIs for our enterprise SaaS platform.",
     ["Angular", "TypeScript", "CSS", "RxJS", "Jest"], "Mid", "Chennai, India"),
    ("Android Developer",
     "Build native Android apps with Kotlin and Jetpack Compose for millions of users.",
     ["Kotlin", "Android", "Jetpack Compose", "Java"], "Mid", "Gurugram, India"),
    ("iOS Developer",
     "Develop delightful iOS experiences using Swift and SwiftUI.",
     ["Swift", "iOS", "SwiftUI", "Xcode"], "Senior", "Bengaluru, India"),
    ("Data Engineer",
     "Design and maintain data pipelines processing terabytes daily with Spark and Airflow.",
     ["Python", "Spark", "Airflow", "Kafka", "Big Data"], "Senior", "Delhi, India"),
    ("Cloud Solutions Architect",
     "Architect secure, cost-effective cloud solutions on Azure for enterprise clients.",
     ["Azure", "Terraform", "Kubernetes", "System Design"], "Lead", "London"),
    ("Cybersecurity Analyst",
     "Monitor, detect, and respond to security threats across our infrastructure.",
     ["Cybersecurity", "Linux", "Networking", "Python"], "Mid", "Noida, India"),
    ("Blockchain Developer",
     "Build smart contracts and decentralized applications on Ethereum.",
     ["Blockchain", "Solidity", "JavaScript", "Web3"], "Senior", "Singapore"),
    ("QA Automation Engineer",
     "Design automated test suites to ensure product quality across releases.",
     ["Selenium", "Cypress", "Test Automation", "Python", "QA"], "Mid", "Kochi, India"),
    ("Junior Frontend Developer",
     "Learn and grow while building UI components with React and Tailwind.",
     ["React", "JavaScript", "HTML", "CSS", "Tailwind CSS"], "Entry", "Ahmedabad, India"),
    ("Site Reliability Engineer",
     "Ensure reliability and performance of production services at scale.",
     ["Kubernetes", "Prometheus", "Grafana", "Go", "Linux"], "Senior", "Remote"),
    ("Product Manager - Fintech",
     "Own the product roadmap for our payments platform and work with cross-functional teams.",
     ["Product Management", "Fintech", "Agile", "Communication"], "Lead", "Mumbai, India"),
    ("AI Research Engineer",
     "Research and build generative AI features using LLMs and modern NLP.",
     ["Python", "LLM", "Generative AI", "PyTorch", "Hugging Face"], "Senior", "San Francisco"),
    ("Backend Developer - Java Spring",
     "Develop robust microservices with Spring Boot for banking applications.",
     ["Java", "Spring Boot", "Microservices", "PostgreSQL"], "Mid", "Jaipur, India"),
    ("Flutter Mobile Developer",
     "Build cross-platform mobile apps with Flutter for our e-commerce brand.",
     ["Flutter", "Dart", "Firebase", "REST APIs"], "Entry", "Indore, India"),
    ("Data Scientist",
     "Apply statistical modeling and ML to solve business problems in retail.",
     ["Python", "Machine Learning", "Pandas", "Scikit-learn", "Statistics"], "Mid", "Bengaluru, India"),
    ("Golang Backend Engineer",
     "Build high-performance backend services in Go for our streaming platform.",
     ["Go", "gRPC", "Redis", "Docker", "Microservices"], "Senior", "Berlin"),
    ("UI/UX Designer",
     "Design intuitive interfaces and prototypes for web and mobile products.",
     ["UI/UX Design", "Figma", "HTML", "CSS"], "Mid", "Hyderabad, India"),
    ("Entry-Level Software Engineer",
     "Kickstart your career building features across our stack with mentorship.",
     ["Python", "JavaScript", "SQL", "Git", "Data Structures"], "Entry", "Remote"),
]


def seed():
    init_db()
    db = SessionLocal()

    try:
        if db.query(User).first():
            print("Database already seeded. Skipping.")
            return

        admin = User(email="admin@example.com", password_hash=hash_password("admin123"), role="admin")
        db.add(admin)
        db.flush()

        candidate = User(email="candidate@example.com", password_hash=hash_password("candidate123"), role="candidate")
        db.add(candidate)
        db.flush()

        for title, desc, skills, level, location in JOBS:
            db.add(JobListing(
                admin_id=admin.id, title=title, description=desc,
                required_skills=skills, experience_level=level,
                location=location, status="open",
            ))

        profile = CandidateProfile(
            candidate_id=candidate.id,
            name="Jane Developer",
            skills=["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
            education=["BS Computer Science - MIT", "ML Certification - Coursera"],
            project_summaries=[
                "Built a microservices platform handling 10k requests/s",
                "Created an open-source data pipeline tool with 500+ stars",
            ],
            preferred_location="Remote",
            role_type="Backend Engineer",
            domain_interest="Healthcare",
        )
        db.add(profile)

        db.commit()
        print(f"Database seeded successfully with {len(JOBS)} jobs!")
        print("  Admin: admin@example.com / admin123")
        print("  Candidate: candidate@example.com / candidate123")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
