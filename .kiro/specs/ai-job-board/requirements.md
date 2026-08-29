# Requirements Document

## Introduction

This document defines the requirements for a Job Board web application with AI-powered candidate matching. The system supports two user roles: Company Admins who manage job listings and review applications, and Candidates who create profiles, browse jobs, and apply. The AI component allows candidates to describe their ideal role in natural language, and the system returns ranked job matches with explanations.

## Glossary

- **System**: The Job Board web application as a whole
- **Admin_Dashboard**: The Company Admin interface for managing jobs and viewing analytics
- **Job_Listing**: A job post containing title, description, required skills, experience level, location, and status
- **Candidate_Profile**: A candidate's stored information including name, skills, education, project summaries, and preferences
- **Matching_Engine**: The AI component that processes natural language queries and ranks job listings by relevance
- **Application**: A submission from a candidate to a specific job listing, containing the candidate's profile details
- **Company_Admin**: A user role that creates and manages job listings, reviews applications, and views analytics
- **Candidate**: A user role that creates a profile, browses jobs, uses AI matching, and applies to listings
- **Match_Explanation**: A brief textual explanation of why a particular job listing matches a candidate's query
- **Application_Status**: The state of an application, one of: Applied, Shortlisted, or Rejected
- **API**: The backend RESTful API built with Python (Flask or FastAPI)
- **Frontend**: The React-based user interface with separate views for Admin and Candidate roles

## Requirements

### Requirement 1: Job Listing Management

**User Story:** As a Company Admin, I want to create, edit, and manage job listings, so that I can advertise open positions to candidates.

#### Acceptance Criteria

1. WHEN a Company_Admin submits a new job listing with title (maximum 150 characters), description (maximum 5000 characters), required skills (1 to 20 skills), experience level (one of: Entry, Mid, Senior, Lead), and location, THE System SHALL create the Job_Listing with a status of "open" and persist it in the database.
2. WHEN a Company_Admin edits an existing Job_Listing that they own, THE System SHALL update the specified fields and persist the changes.
3. WHEN a Company_Admin changes the status of a Job_Listing that they own, THE System SHALL update the status to the specified value (open or closed).
4. THE System SHALL require all Job_Listing fields (title, description, required skills, experience level, location) to be non-empty and within the defined length limits before creating or updating a listing.
5. IF a Company_Admin attempts to create or edit a Job_Listing with missing or invalid required fields, THEN THE System SHALL return a validation error indicating which fields are missing or invalid.
6. IF a Company_Admin attempts to edit or change the status of a Job_Listing that does not exist, THEN THE System SHALL return an error indicating the listing was not found.
7. IF a Company_Admin attempts to edit or change the status of a Job_Listing they do not own, THEN THE System SHALL reject the request and return an authorization error.
8. IF a Company_Admin attempts to set a Job_Listing status to a value other than "open" or "closed", THEN THE System SHALL return a validation error indicating the allowed status values.

### Requirement 2: Candidate Profile Management

**User Story:** As a Candidate, I want to create and manage my profile, so that I can present my qualifications to potential employers.

#### Acceptance Criteria

1. WHEN a Candidate submits profile information including name, skills (1 to 50 entries, each up to 100 characters), education (1 to 20 entries), and project summaries (0 to 20 entries), THE System SHALL create the Candidate_Profile and persist it in the database.
2. WHEN a Candidate updates their Candidate_Profile, THE System SHALL persist only the modified fields and retain all unmodified fields unchanged.
3. THE System SHALL store Candidate preferences (preferred location, role type, and domain interest) as optional fields, each up to 200 characters in length.
4. IF a Candidate attempts to create a profile without providing a name or without providing at least one skill, THEN THE System SHALL return a validation error indicating which required fields are missing.
5. IF a Candidate attempts to create a Candidate_Profile when one already exists for that Candidate, THEN THE System SHALL reject the request and return an error indicating a profile already exists.

### Requirement 3: AI-Powered Job Matching

**User Story:** As a Candidate, I want to describe what I am looking for in natural language, so that the system can find and rank relevant job listings for me.

#### Acceptance Criteria

1. WHEN a Candidate submits a natural language query describing their desired role, THE Matching_Engine SHALL return a ranked list of at most 20 Job_Listings ordered by descending match score, where each result includes a numeric match score between 0 and 100.
2. WHEN the Matching_Engine returns results, THE System SHALL include a Match_Explanation for each returned Job_Listing describing why it is relevant to the query.
3. THE Matching_Engine SHALL only return Job_Listings with a status of "open".
4. IF a Candidate submits a query that is empty or contains only whitespace, THEN THE System SHALL return a validation error requesting a non-empty description.
5. IF a Candidate submits a query exceeding 1000 characters, THEN THE System SHALL return a validation error indicating the query exceeds the maximum allowed length.
6. IF no Job_Listings match the candidate's query, THEN THE System SHALL return an empty result set with a message indicating no matches were found.
7. IF the Matching_Engine is unavailable or fails to process the query, THEN THE System SHALL return an error indicating that the matching service is temporarily unavailable and the Candidate should retry later.

### Requirement 4: Job Application Submission

**User Story:** As a Candidate, I want to apply to a job listing, so that I can express my interest in a position.

#### Acceptance Criteria

1. WHEN a Candidate applies to a Job_Listing, THE System SHALL create an Application referencing the Candidate_Profile and set the Application_Status to "Applied".
2. THE System SHALL associate each Application with exactly one Candidate_Profile and one Job_Listing.
3. IF a Candidate attempts to apply to a Job_Listing that has a status of "closed", THEN THE System SHALL reject the application and return an error indicating the listing is no longer accepting applications.
4. IF a Candidate attempts to apply to a Job_Listing they have already applied to, THEN THE System SHALL reject the duplicate application and return an error.
5. IF a Candidate attempts to apply without having a Candidate_Profile, THEN THE System SHALL reject the application and return an error indicating that a profile must be created first.
6. WHEN an Application is successfully created, THE System SHALL return a confirmation response including the Application identifier and the initial status of "Applied".

### Requirement 5: Application Review and Status Management

**User Story:** As a Company Admin, I want to view applications for my job listings and update their status, so that I can manage my hiring pipeline.

#### Acceptance Criteria

1. WHEN a Company_Admin requests applications for a specific Job_Listing they own, THE System SHALL return all Applications associated with that listing, ordered by submission date (most recent first).
2. WHEN a Company_Admin updates an Application_Status, THE System SHALL change the status to the specified value (Applied, Shortlisted, or Rejected) and persist the change.
3. IF a Company_Admin attempts to set an Application_Status to a value other than Applied, Shortlisted, or Rejected, THEN THE System SHALL return a validation error indicating the allowed status values.
4. IF a Company_Admin attempts to view applications or update an Application_Status for a Job_Listing they do not own, THEN THE System SHALL reject the request and return an authorization error.

### Requirement 6: Admin Dashboard Analytics

**User Story:** As a Company Admin, I want to view analytics about my job listings, so that I can understand applicant trends and pipeline status.

#### Acceptance Criteria

1. WHEN a Company_Admin accesses the Admin_Dashboard, THE System SHALL display the count of applications per Job_Listing, scoped to only the Job_Listings owned by that Company_Admin.
2. WHEN a Company_Admin accesses the Admin_Dashboard, THE System SHALL display the count of applications per skill across all applicants to that Company_Admin's Job_Listings.
3. WHEN a Company_Admin accesses the Admin_Dashboard, THE System SHALL display the count of applications grouped by Application_Status (Applied, Shortlisted, Rejected), scoped to only the Job_Listings owned by that Company_Admin.
4. IF a Company_Admin accesses the Admin_Dashboard and has no Job_Listings or no Applications exist for their listings, THEN THE System SHALL display zero counts for each analytics metric.

### Requirement 7: Job Search and Filtering

**User Story:** As a Candidate, I want to search and filter job listings, so that I can find relevant positions without using the AI matching feature.

#### Acceptance Criteria

1. WHEN a Candidate searches for jobs by skill, THE System SHALL return all open Job_Listings where at least one required skill matches the specified skill using case-insensitive exact matching.
2. WHEN a Candidate filters jobs by location, THE System SHALL return all open Job_Listings whose location matches the specified location using case-insensitive exact matching.
3. WHEN a Candidate filters jobs by experience level, THE System SHALL return all open Job_Listings whose experience level matches the specified experience level exactly.
4. WHEN a Candidate applies multiple filters simultaneously, THE System SHALL return only Job_Listings matching all specified filter criteria (AND logic).
5. THE System SHALL only include Job_Listings with a status of "open" in search and filter results.
6. IF a Candidate submits a search or filter request with all filter fields empty, THEN THE System SHALL return all open Job_Listings without applying any filter.
7. IF no open Job_Listings match the specified search or filter criteria, THEN THE System SHALL return an empty result set.
8. THE System SHALL return search and filter results ordered by creation date, most recent first.

### Requirement 8: Backend API

**User Story:** As a developer, I want a well-structured RESTful API, so that the frontend can interact with all system features reliably.

#### Acceptance Criteria

1. THE API SHALL expose RESTful endpoints for all Job_Listing, Candidate_Profile, Application, and Matching_Engine operations, and SHALL return all responses in JSON format.
2. WHEN an API request succeeds, THE API SHALL return the appropriate HTTP status code (200 for retrieval, 200 for update, 201 for creation, 204 for deletion).
3. IF an API request contains invalid data, THEN THE API SHALL return HTTP status code 400 with a JSON response containing an error message that identifies which fields failed validation and why.
4. IF an API request references a resource that does not exist, THEN THE API SHALL return HTTP status code 404 with a JSON response containing an error message indicating the resource type and identifier that was not found.
5. IF an unexpected server error occurs, THEN THE API SHALL return HTTP status code 500 with a generic error message that does not expose internal details such as stack traces, database queries, or file paths.
6. THE API SHALL be implemented using Python with Flask or FastAPI framework.
7. WHEN a list endpoint returns more than 20 results, THE API SHALL paginate the response with a maximum of 20 items per page and include the total count, current page number, and total number of pages in the response.

### Requirement 9: Frontend User Interface

**User Story:** As a user, I want a clean and functional interface, so that I can interact with the system efficiently.

#### Acceptance Criteria

1. THE Frontend SHALL provide a separate view for Company_Admin operations (job management, application review, dashboard).
2. THE Frontend SHALL provide a separate view for Candidate operations (profile management, job search, AI matching, applications).
3. THE Frontend SHALL be implemented using React.
4. WHEN a user performs an action that results in an error, THE Frontend SHALL display the error message returned by the API in a visible notification that auto-dismisses after 5 seconds or can be manually dismissed.
5. WHEN a user submits a form, THE Frontend SHALL validate required fields before sending the request to the API, and SHALL display inline validation messages next to each invalid field.
6. WHILE an API request is in progress, THE Frontend SHALL display a loading indicator and disable the submit button to prevent duplicate submissions.

### Requirement 10: Project Structure and Documentation

**User Story:** As a developer, I want clear documentation and organized code, so that I can understand and maintain the project.

#### Acceptance Criteria

1. THE System SHALL organize source code into distinct top-level directories separating backend code and frontend code, with no backend source files in the frontend directory and no frontend source files in the backend directory.
2. THE System SHALL include a README file at the project root containing the following sections: (a) tech stack listing all frameworks and languages used, (b) architecture decisions explaining the separation of concerns and key design choices, (c) setup instructions specifying how to install dependencies and start both the backend and frontend, and (d) assumptions listing any constraints or decisions made during development.
3. WHEN a developer follows the setup instructions in the README, THE System SHALL be runnable by executing the documented commands to install dependencies and start both the backend API and the Frontend.
