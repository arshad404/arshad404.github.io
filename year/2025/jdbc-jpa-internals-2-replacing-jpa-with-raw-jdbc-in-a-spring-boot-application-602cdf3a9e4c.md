---
published: 2025-01-19T11:35:46Z
source: medium
medium_url: https://arshad404.medium.com/jdbc-jpa-internals-2-replacing-jpa-with-raw-jdbc-in-a-spring-boot-application-602cdf3a9e4c
---

# Replacing JPA with JDBC in Spring Boot

#database #programming #java #sql #coding

## Replacing JPA with JDBC

Same blog I have explained in this youtube video, if you are a video person please consider watching this video.

In this follow-up blog, we’ll extend our previous project by replacing JPA with raw JDBC. Using JDBC gives us more control over database interactions and reduces dependencies, albeit at the cost of more boilerplate code. This guide will demonstrate how to modify the previous Spring Boot application to use raw JDBC for managing users.

## Step 1: Setting Up JDBC in Spring Boot

Spring Boot supports JDBC out-of-the-box with its DataSource abstraction. If your application already includes the PostgreSQL driver, you’re all set to begin.

### Dependencies

Ensure your pom.xml includes the PostgreSQL driver:

```
<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

No additional dependencies are required for using raw JDBC.

## Step 2: Replacing the JPA Repository

The core change involves replacing the UserRepositoryJPA interface with a service layer that uses raw JDBC. Create a new class called UserRepositoryJDBC in the repository package:

```
@Service
public class UserRepositoryJDBC {
    private final DataSource dataSource;
    @Autowired
    public UserRepositoryJDBC(DataSource dataSource) {
        this.dataSource = dataSource;
    }
    public List<User> getUsers() throws SQLException {
        String sqlQuery = "SELECT id, name, email FROM users";
        List<User> users = new ArrayList<>();
        try (Connection connection = dataSource.getConnection()) {
            PreparedStatement preparedStatement = connection.prepareStatement(sqlQuery);
            try (ResultSet resultSet = preparedStatement.executeQuery()) {
                while (resultSet.next()) {
                    User user = new User(
                            resultSet.getLong("id"),
                            resultSet.getString("name"),
                            resultSet.getString("email")
                    );
                    users.add(user);
                }
            }
            return users;
        } catch (SQLException e) {
            throw new SQLException(e);
        }
    }
    public int addUser(User user) throws SQLException {
        String sqlQuery = "INSERT INTO users (name, email) VALUES (?, ?)";
        try (Connection connection = dataSource.getConnection()) {
            PreparedStatement preparedStatement = connection.prepareStatement(sqlQuery);
            preparedStatement.setString(1, user.getName());
            preparedStatement.setString(2, user.getEmail());
            return preparedStatement.executeUpdate();
        } catch (SQLException e) {
            throw new SQLException(e);
        }
    }
}
```

This class defines methods for retrieving and adding users using SQL queries. Here are the key methods:

- getUsers(): Executes a SELECT query to retrieve all users.

- addUser(User user): Executes an INSERT query to add a new user.

## Step 3: Updating the Controller

Update the UserController to use the new UserRepositoryJDBC service. Replace the UserRepositoryJPA dependency with UserRepositoryJDBC:

```
@RestController
@RequestMapping("/api/users")
public class UserController {
private final UserRepositoryJDBC userRepositoryJDBC;
    @Autowired
    public UserController(UserRepositoryJDBC userRepositoryJDBC) {
        this.userRepositoryJDBC = userRepositoryJDBC;
    }
    @GetMapping("/")
    public List<User> getAllUsers() throws SQLException {
        return userRepositoryJDBC.getUsers();
    }
    @PostMapping("/")
    public String addUser(@RequestBody User user) throws SQLException {
        int rowsInserted = userRepositoryJDBC.addUser(user);
        return rowsInserted > 0 ? "User added successfully" : "Failed to add user";
    }
}
```

This controller now uses raw JDBC to handle requests.

## Step 4: Testing the Application

Run the Application:

Start the Spring Boot application from the main method as usual.

Test the Endpoints:

- GET all users:

```curl -X GET http://localhost:8080/api/users/
```

- POST a new user:

```curl -X POST -H "Content-Type: application/json" -d '{"name":"John Doe","email":"john.doe@example.com"}' http://localhost:8080/api/users/
```

## Thank you for being a part of the community

Before you go:

- Be sure to clap and follow the writer ️👏️️

- Follow us: X | LinkedIn | YouTube | Newsletter | Podcast

- Check out CoFeed, the smart way to stay up-to-date with the latest in tech 🧪

- Start your own free AI-powered blog on Differ 🚀

- Join our content creators community on Discord 🧑🏻‍💻

- For more content, visit plainenglish.io + stackademic.com
