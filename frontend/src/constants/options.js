// Shared option lists for locations, skills, and experience levels.

export const LEVELS = ['Entry', 'Mid', 'Senior', 'Lead']

// Indian States (28)
export const INDIAN_STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
]

// Indian Union Territories (8)
export const INDIAN_UNION_TERRITORIES = [
  'Andaman and Nicobar Islands', 'Chandigarh',
  'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Jammu and Kashmir',
  'Ladakh', 'Lakshadweep', 'Puducherry',
]

// Major Indian cities (tech hubs and metros)
export const INDIAN_CITIES = [
  'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune',
  'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore',
  'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Ghaziabad', 'Ludhiana',
  'Coimbatore', 'Kochi', 'Chandigarh', 'Guwahati', 'Thiruvananthapuram',
  'Bhubaneswar', 'Mysuru', 'Noida', 'Gurugram', 'Nashik', 'Rajkot', 'Ranchi',
]

// Countries of the world
export const COUNTRIES = [
  'Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Armenia', 'Australia',
  'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium',
  'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Bulgaria',
  'Cambodia', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia',
  'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic',
  'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Finland',
  'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Honduras',
  'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq',
  'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
  'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg',
  'Malaysia', 'Maldives', 'Malta', 'Mexico', 'Mongolia', 'Morocco', 'Nepal',
  'Netherlands', 'New Zealand', 'Nigeria', 'North Macedonia', 'Norway', 'Oman',
  'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines', 'Poland',
  'Portugal', 'Qatar', 'Romania', 'Russia', 'Saudi Arabia', 'Serbia',
  'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 'South Korea', 'Spain',
  'Sri Lanka', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Tunisia',
  'Turkey', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
  'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam',
]

// Major global tech-hub cities
export const GLOBAL_CITIES = [
  'New York', 'San Francisco', 'Seattle', 'Austin', 'Boston', 'London',
  'Berlin', 'Amsterdam', 'Dublin', 'Paris', 'Toronto', 'Vancouver', 'Sydney',
  'Melbourne', 'Singapore', 'Dubai', 'Tokyo', 'Tel Aviv', 'Zurich', 'Munich',
  'Stockholm', 'Barcelona', 'Lisbon', 'Warsaw',
]

// Combined location list: Remote/Hybrid first, then Indian locations, then world.
export const LOCATIONS = [
  'Remote', 'Hybrid', 'On-site',
  ...INDIAN_CITIES.map((c) => `${c}, India`),
  ...INDIAN_STATES.map((s) => `${s}, India`),
  ...INDIAN_UNION_TERRITORIES.map((u) => `${u}, India`),
  ...GLOBAL_CITIES,
  ...COUNTRIES,
]

// Comprehensive skills list across many domains.
export const SKILLS = [
  // Languages
  'Python', 'JavaScript', 'TypeScript', 'Java', 'C', 'C++', 'C#', 'Go', 'Rust',
  'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'Dart', 'Objective-C',
  'Perl', 'Haskell', 'Elixir', 'Clojure', 'Lua', 'MATLAB', 'Julia', 'Shell',
  'Bash', 'PowerShell', 'SQL', 'HTML', 'CSS', 'Sass',
  // Frontend
  'React', 'Angular', 'Vue.js', 'Next.js', 'Nuxt.js', 'Svelte', 'Redux',
  'Tailwind CSS', 'Bootstrap', 'jQuery', 'Webpack', 'Vite', 'Material UI',
  // Backend / Frameworks
  'Node.js', 'Express', 'FastAPI', 'Flask', 'Django', 'Spring Boot', 'Spring',
  'Laravel', 'Ruby on Rails', 'ASP.NET', '.NET Core', 'NestJS', 'GraphQL',
  'REST APIs', 'gRPC', 'Microservices',
  // Databases
  'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Redis', 'Cassandra',
  'DynamoDB', 'Oracle', 'SQL Server', 'Elasticsearch', 'Neo4j', 'MariaDB',
  'Firebase',
  // Cloud / DevOps
  'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
  'Ansible', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'CI/CD', 'Linux',
  'Nginx', 'Apache', 'Prometheus', 'Grafana', 'Helm', 'CloudFormation',
  'Serverless', 'Lambda',
  // Data / AI / ML
  'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
  'Scikit-learn', 'Pandas', 'NumPy', 'NLP', 'Computer Vision', 'MLOps',
  'Data Science', 'Data Engineering', 'Data Analysis', 'Spark', 'Hadoop',
  'Kafka', 'Airflow', 'Tableau', 'Power BI', 'Statistics', 'Big Data',
  'LLM', 'Generative AI', 'OpenAI API', 'LangChain', 'Hugging Face',
  // Mobile
  'React Native', 'Flutter', 'Android', 'iOS', 'SwiftUI', 'Jetpack Compose',
  'Xamarin', 'Ionic',
  // Testing / QA
  'Jest', 'Cypress', 'Selenium', 'Playwright', 'Pytest', 'JUnit', 'Mocha',
  'Testing', 'Test Automation', 'QA',
  // Tools / Practices
  'Git', 'Agile', 'Scrum', 'Jira', 'Figma', 'REST', 'OAuth', 'JWT',
  'WebSockets', 'RabbitMQ', 'Celery', 'System Design', 'Design Patterns',
  'Data Structures', 'Algorithms', 'OOP', 'Functional Programming',
  // Domains
  'Healthcare', 'Fintech', 'E-commerce', 'Cybersecurity', 'Blockchain',
  'IoT', 'Game Development', 'AR/VR', 'Embedded Systems', 'Networking',
  // Soft / other
  'Product Management', 'UI/UX Design', 'Technical Writing', 'Leadership',
  'Communication', 'Problem Solving',
]
