#!/bin/bash
# End-to-end demo of the AI Job Board — exercises every feature via the API.
set -e
BASE="http://localhost:8000/api"

sep() { echo ""; echo "=================================================="; echo "  $1"; echo "=================================================="; }
jq_or_cat() { python3 -m json.tool 2>/dev/null || cat; }

sep "1. AUTH — Register a new Company Admin"
ADMIN=$(curl -s -X POST $BASE/auth/register -H "Content-Type: application/json" \
  -d '{"email":"acme@demo.com","password":"secret1","role":"admin"}')
echo "$ADMIN" | jq_or_cat
ATOKEN=$(echo "$ADMIN" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

sep "2. AUTH — Register a new Candidate"
CAND=$(curl -s -X POST $BASE/auth/register -H "Content-Type: application/json" \
  -d '{"email":"sam@demo.com","password":"secret1","role":"candidate"}')
echo "$CAND" | jq_or_cat
CTOKEN=$(echo "$CAND" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

sep "3. ADMIN — Create a job listing (title, skills, level, location)"
JOB=$(curl -s -X POST $BASE/jobs -H "Content-Type: application/json" -H "Authorization: Bearer $ATOKEN" \
  -d '{"title":"AI Engineer - Healthcare","description":"Build ML models for patient outcome prediction using Python and PyTorch in a fast-moving healthcare startup.","required_skills":["Python","PyTorch","NLP","Healthcare"],"experience_level":"Senior","location":"Remote"}')
echo "$JOB" | jq_or_cat
JOBID=$(echo "$JOB" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

sep "4. ADMIN — Validation error (empty title, no skills) => HTTP 400"
curl -s -o /tmp/resp -w "HTTP %{http_code}\n" -X POST $BASE/jobs -H "Content-Type: application/json" -H "Authorization: Bearer $ATOKEN" \
  -d '{"title":"","description":"x","required_skills":[],"experience_level":"Mid","location":"NY"}'
cat /tmp/resp | jq_or_cat

sep "5. CANDIDATE — Create profile"
curl -s -X POST $BASE/candidates/profile -H "Content-Type: application/json" -H "Authorization: Bearer $CTOKEN" \
  -d '{"name":"Sam Rivera","skills":["Python","PyTorch","NLP","SQL"],"education":["MS Data Science - Stanford"],"project_summaries":["Built a clinical NLP pipeline"],"preferred_location":"Remote","role_type":"ML Engineer","domain_interest":"Healthcare"}' | jq_or_cat

sep "6. CANDIDATE — AI Matching (natural language query)"
echo 'Query: "I want a Python machine learning role at a healthcare startup, remote"'
echo ""
curl -s -X POST $BASE/matching -H "Content-Type: application/json" -H "Authorization: Bearer $CTOKEN" \
  -d '{"query":"I want a Python machine learning role at a healthcare startup, remote"}' | jq_or_cat

sep "7. CANDIDATE — Search jobs by skill filter (skill=PyTorch)"
curl -s "$BASE/jobs?skill=PyTorch" -H "Authorization: Bearer $CTOKEN" | jq_or_cat

sep "8. CANDIDATE — Apply to the job => HTTP 201"
curl -s -X POST $BASE/jobs/$JOBID/apply -H "Authorization: Bearer $CTOKEN" | jq_or_cat

sep "9. CANDIDATE — Duplicate apply => HTTP 409 (rejected)"
curl -s -o /tmp/resp -w "HTTP %{http_code}\n" -X POST $BASE/jobs/$JOBID/apply -H "Authorization: Bearer $CTOKEN"
cat /tmp/resp | jq_or_cat

sep "10. ADMIN — View applications for the job"
APPS=$(curl -s "$BASE/jobs/$JOBID/applications" -H "Authorization: Bearer $ATOKEN")
echo "$APPS" | jq_or_cat
APPID=$(echo "$APPS" | python3 -c "import sys,json;print(json.load(sys.stdin)['items'][0]['id'])")

sep "11. ADMIN — Advance pipeline: Applied -> Shortlisted"
curl -s -X PATCH $BASE/applications/$APPID/status -H "Content-Type: application/json" -H "Authorization: Bearer $ATOKEN" \
  -d '{"status":"Shortlisted"}' | jq_or_cat

sep "12. ADMIN — Dashboard analytics (per-job, skills, pipeline)"
curl -s $BASE/admin/dashboard -H "Authorization: Bearer $ATOKEN" | jq_or_cat

sep "13. CANDIDATE — My applications (status now Shortlisted)"
curl -s $BASE/candidates/applications -H "Authorization: Bearer $CTOKEN" | jq_or_cat

sep "14. SECURITY — Candidate tries to create a job => HTTP 403"
curl -s -o /tmp/resp -w "HTTP %{http_code}\n" -X POST $BASE/jobs -H "Content-Type: application/json" -H "Authorization: Bearer $CTOKEN" \
  -d '{"title":"Hack","description":"x","required_skills":["a"],"experience_level":"Mid","location":"NY"}'
cat /tmp/resp | jq_or_cat

echo ""
echo "=================================================="
echo "  DEMO COMPLETE — all features exercised"
echo "=================================================="
