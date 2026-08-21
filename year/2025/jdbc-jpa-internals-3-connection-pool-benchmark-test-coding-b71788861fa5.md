---
published: 2025-01-21T16:05:51Z
source: medium
medium_url: https://arshad404.medium.com/jdbc-jpa-internals-3-connection-pool-benchmark-test-coding-b71788861fa5
---

# JDBC Connection Pools in Spring Boot: 3206ms to 372ms

#sql #java #connection-pool #postgresql #database

## Building a Connection Pool

Same blog I have explained in this youtube video, if you are a video person please consider watching this video.

In any application interacting with a database, the efficiency of managing database connections plays a significant role in overall performance. In this blog, we will explore how to create a database connection pool programmatically in a Spring Boot application, compare its performance against non-pooling implementations, and understand the execution flow from the application to the database.

To provide insights, we benchmarked the time taken to execute database operations using a connection pool versus without one. With a connection pool, the time taken was 373 ms, while without it, it shot up to 3206 ms.

## What is a Connection Pool?

A connection pool is a cache of reusable database connections maintained in memory. Instead of creating a new connection for every database request, the pool allows applications to reuse existing connections, reducing the overhead of connection creation and teardown.

## Why Use a Connection Pool?

- Performance: Reusing connections reduces the time spent in creating and closing database connections.

- Resource Optimization: Limits the number of simultaneous connections to the database, preventing resource exhaustion.

- Scalability: Handles high concurrent user requests more effectively by managing connections efficiently.

## Application to Database Flow

Here is a high-level flow of how a request from the application interacts with the database:

- Application: Initiates the request.

- DataSource: Acts as a factory for managing connections (especially when pooling is used).

- DriverManager: Selects the appropriate database driver based on the connection URL.

- Driver: Manages the database-specific implementation of the JDBC API.

- Connection: Represents the session between the application and the database.

- SocketFactory: Creates a socket to establish a network connection to the database.

- Socket: Transmits SQL queries and receives responses.

- RDBMS: Processes the SQL queries and sends back the results.

## Codebase: Setting Up Connection Pool Programmatically

Here is the code for creating a connection pool programmatically in a Spring Boot application using HikariCP:

### With Connection Pool

```import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class ConnectionPoolExample {

    public static DataSource createDataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://localhost:5432/your_db");
        config.setUsername("user");
        config.setPassword("password");
        config.setMaximumPoolSize(10);
        return new HikariDataSource(config);
    }

    public static void main(String[] args) throws Exception {
        DataSource dataSource = createDataSource();
        long start = System.currentTimeMillis();

        try (Connection connection = dataSource.getConnection()) {
            PreparedStatement statement = connection.prepareStatement("SELECT * FROM employees");
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                System.out.println("Employee Name: " + resultSet.getString("name"));
            }
        }

        long end = System.currentTimeMillis();
        System.out.println("Time taken with connection pool: " + (end - start) + " ms");
    }
}
```

### Without Connection Pool

```import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class NoConnectionPoolExample {

    public static Connection createConnection() throws Exception {
        return DriverManager.getConnection(
            "jdbc:postgresql://localhost:5432/your_db",
            "user",
            "password"
        );
    }

    public static void main(String[] args) throws Exception {
        long start = System.currentTimeMillis();

        try (Connection connection = createConnection()) {
            PreparedStatement statement = connection.prepareStatement("SELECT * FROM employees");
            ResultSet resultSet = statement.executeQuery();

            while (resultSet.next()) {
                System.out.println("Employee Name: " + resultSet.getString("name"));
            }
        }

        long end = System.currentTimeMillis();
        System.out.println("Time taken without connection pool: " + (end - start) + " ms");
    }
}
```

## Performance Benchmark Results

We benchmarked the time taken to execute the same query using both approaches:

- Time Take With Connection Pool 373 ms

- Time Take Without Connection Pool3206 ms

### Key Observations

With Connection Pool:

- The connections are reused from the pool, drastically reducing the time needed for connection setup and teardown.

- Ideal for applications with frequent database interactions.

Without Connection Pool:

- A new connection is created and destroyed for every request, leading to significant overhead.

- This approach becomes a bottleneck under high concurrency.

## Execution Flow in Detail

Let’s break down the flow of execution:

- Application sends a request to the database.

- DataSource or DriverManager facilitates obtaining a connection.

- With Connection Pool: DataSource reuses a connection from the pool.

- Without Connection Pool: DriverManager creates a new connection every time.

- The Driver handles translating the JDBC API calls into database-specific commands.

- A SocketFactory creates a socket to establish a network connection with the database server.

- A Socket transmits the SQL query to the database and receives the response.

- The RDBMS executes the query and sends the result back through the socket.

## Conclusion

Using a connection pool significantly boosts performance by reusing existing connections and reducing the overhead of connection management. This is particularly beneficial in applications with high database interaction.

If you’re building a Spring Boot application or any application requiring database connectivity, incorporating a connection pool should be a top priority for optimal performance.

For more insights, check out the CodePiper — YouTube explaining this codebase in detail, where we walk through the implementation and discuss the benchmarking results. Happy coding!

## Thank you for being a part of the community

Before you go:

- Be sure to clap and follow the writer ️👏️️

- Follow us: X | LinkedIn | YouTube | Newsletter | Podcast

- Check out CoFeed, the smart way to stay up-to-date with the latest in tech 🧪

- Start your own free AI-powered blog on Differ 🚀

- Join our content creators community on Discord 🧑🏻‍💻

- For more content, visit plainenglish.io + stackademic.com
