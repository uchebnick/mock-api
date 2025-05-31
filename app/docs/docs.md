# Counter Service API Documentation

## Endpoints

### GET /count
- **Summary**: Retrieve current counter value
- **Returns**: JSON object containing count
- **Example Response**:
  ```json
  {"count": 42}
  ```

### POST /increment
- **Summary**: Increment counter by 1
- **Produces**: No request body required
- **Example Response**:
  ```json
  {"count": 43}
  ```

## Database Models

| Table      | Columns             |
|------------|---------------------|
| counters   | - id (primary key, integer) |
|            | - count (integer)