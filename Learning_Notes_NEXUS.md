# NEXUS — Module 05 Learning Notes

## 1. FastAPI and Web Frameworks
FastAPI is a modern Python framework for building APIs. It uses Python type hints for validation and generates interactive OpenAPI documentation. Routes connect HTTP methods and URL paths to Python functions.

## 2. Routing, Endpoints and HTTP Methods
GET retrieves resources; POST creates resources; PUT replaces a resource; PATCH updates selected fields; DELETE removes a resource. An endpoint is a method and path combination such as GET /tasks.

## 3. Database Integration and SQLite
SQLite is a lightweight relational database stored in a file. SQLAlchemy ORM maps Python classes to database tables and helps perform database operations using Python objects.

## 4. CRUD Operations
Create inserts a record; Read retrieves records; Update changes stored values; Delete removes records. The NEXUS API applies CRUD operations to task records.

## 5. Authentication and JWT
Authentication verifies a user's identity. NEXUS hashes passwords using PBKDF2-HMAC-SHA256 and issues a signed JWT access token after login. Protected routes require a Bearer token. Keep signing secrets private and use HTTPS in deployed systems.

## 6. Schema Validation with Pydantic
Pydantic models define expected request and response structures. Field constraints validate lengths and allowed values, helping reject malformed input before business logic runs.

## 7. API Testing
Automated tests check status codes, response data and CRUD behavior. FastAPI's TestClient can exercise endpoints without manually opening a browser. Run tests with pytest -q.

## 8. NEXUS Architecture
app/main.py contains endpoints; app/models.py defines SQLAlchemy tables; app/schemas.py defines Pydantic schemas; app/database.py configures SQLite sessions; app/security.py contains password hashing and JWT helpers; tests/test_api.py checks the API.

## 9. API Documentation
FastAPI automatically provides Swagger UI at /docs and ReDoc at /redoc. These pages describe routes, request schemas, response models and status codes.

## 10. Production Considerations
For production, use a strong managed secret, HTTPS, rate limiting, refresh-token rotation, database migrations, backups, logging, monitoring and a security review. This project is an educational starter, not a production banking or enterprise service.

## Practice Tasks
1. Add a due_date field to tasks.
2. Add a priority-based sorting option.
3. Add a task count by status endpoint.
4. Write tests for invalid login and unauthorized task access.
5. Add database migrations and environment-based configuration.