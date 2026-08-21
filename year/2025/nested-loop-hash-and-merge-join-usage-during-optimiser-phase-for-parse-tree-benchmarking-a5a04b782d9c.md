---
published: 2025-01-25T19:23:42Z
source: medium
medium_url: https://arshad404.medium.com/nested-loop-hash-and-merge-join-usage-during-optimiser-phase-for-parse-tree-benchmarking-a5a04b782d9c
---

# Comparing SQL Join Strategies: Nested Loop, Hash Join, and Merge Join

#java #coding #database #sql #programming

## Comparing SQL Join Strategies

Same blog I have explained more in this youtube video, if you are a video person please consider watching this video.

In this blog, we will explore the three fundamental SQL join types — Nested Loop Join, Hash Join, and Merge Join — through a practical demonstration. We’ll set up a PostgreSQL database using Docker, create example tables, populate them with data, and run queries to compare the performance of each join type. Let’s dive in!

Little backgroud, Join Types are used in the optimiser phase. When you give the query, it is parsed by the parser and parser passed it to the Optimiser and Optimiser work is to choose the right join type for the query.

https://youtu.be/ZDAd6_HxF2k

## Results of the below benchmarking result

Here are the execution times for each join type:

- Nested Loop Joins: 950.50 ms

- Merge Join: 921.93 ms

- Hash Join: 611.54 ms

## Prerequisites

Before starting, ensure you have Docker installed on your machine. If not, you can download it from Docker’s official site.

## Setting Up the Environment

Run a PostgreSQL container:

```docker run --name postgres-demo -e POSTGRES_PASSWORD=postgres -d -p 5432:5432 postgres
```

Access the PostgreSQL instance:

```docker exec -it postgres-demo psql -U postgres
```

Create the required tables:

```CREATE TABLE employees (     id SERIAL PRIMARY KEY,     name TEXT NOT NULL,     department_id INT );  CREATE TABLE departments (     id SERIAL PRIMARY KEY,     name TEXT NOT NULL );
```

Insert sample data:

```Insert departments INSERT INTO departments (name) SELECT 'Department ' || generate_series(1, 5);  -- Insert employees INSERT INTO employees (name, department_id) SELECT 'Employee ' || generate_series(1, 10000), (random() * 5 + 1)::INT;
```

Now, we have a departments table with 5 entries and an employees table with 10,000 entries, each associated with a random department.

## Benchmarking Different Join Types

PostgreSQL uses different strategies to execute joins based on query requirements, table size, and configuration settings. Let’s analyze each join type in detail.

## 1. Nested Loop Join

Configuration:

```SET enable_hashjoin = off;
SET enable_mergejoin = off;
```

Query Execution:

```EXPLAIN ANALYZE
SELECT e.id, e.name, d.name
FROM employees e
JOIN departments d
ON e.department_id = d.id;
```

## How It Works

- Iterates over each row in one table (outer table) and searches for matching rows in the other table (inner table).

- Suitable for smaller datasets or when indexes are available on the join condition.

Performance:

- Nested loops have quadratic time complexity in the worst case.

- In this experiment, it performed slower compared to other join types due to the large number of rows.

## 2. Hash Join

Configuration:

```SET enable_hashjoin = on;
SET enable_mergejoin = off;
SET enable_nestloop = off;
```

Query Execution:

```EXPLAIN ANALYZE
SELECT e.id, e.name, d.name
FROM employees e
JOIN departments d
ON e.department_id = d.id;
```

## How It Works

- Builds a hash table on the smaller table using the join condition.

- Scans the larger table and probes the hash table for matches.

- Ideal for large datasets without pre-sorted data.

Performance:

- Hash Join was the fastest in this experiment due to efficient in-memory operations.

- Requires sufficient memory for the hash table; otherwise, performance may degrade.

## 3. Merge Join

Configuration:

```SET enable_mergejoin = on;
SET enable_hashjoin = off;
SET enable_nestloop = off;
```

Query Execution:

```EXPLAIN ANALYZE
SELECT e.id, e.name, d.name
FROM employees e
JOIN departments d
ON e.department_id = d.id;
```

## How It Works

- Requires both tables to be sorted on the join key.

- Scans both tables sequentially and merges matching rows.

- Suitable for sorted datasets or queries involving range scans.

Performance:

- Merge Join performed better than Nested Loop but was slower than Hash Join due to sorting overhead.

- Best for pre-sorted data or when an index can efficiently retrieve sorted rows.

## Comparative Analysis

Join TypeExecution TimeBest Use CaseNested Loop12.652 msSmall datasets or when indexes are available.Hash Join4.108 msLarge datasets with sufficient memory.Merge Join5.740 msSorted datasets or range-based conditions.

## Key Takeaways

- Nested Loop Join is simple but can be inefficient for large datasets.

- Hash Join excels with larger datasets and is generally faster if memory allows.

- Merge Join is a balanced choice when dealing with sorted data.

## Conclusion

This experiment highlights how PostgreSQL selects join algorithms based on the query and dataset characteristics. Here’s a quick summary:

- Nested Loop Joins: Suitable for small datasets and indexed lookups but slow for large tables.

- Hash Joins: Efficient for large, unsorted datasets.

- Merge Joins: Ideal for sorted datasets or queries that can leverage indexes.

By understanding these join types, you can optimize your queries and database design to achieve better performance. Try running these experiments on your own database to gain deeper insights into how join operations work!

Please Clap, Follow & Subscribe to my Youtube.

## Thank you for being a part of the community

Before you go:

- Be sure to clap and follow the writer ️👏️️

- Follow us: X | LinkedIn | YouTube | Newsletter | Podcast

- Check out CoFeed, the smart way to stay up-to-date with the latest in tech 🧪

- Start your own free AI-powered blog on Differ 🚀

- Join our content creators community on Discord 🧑🏻‍💻

- For more content, visit plainenglish.io + stackademic.com

Nested Loop, Hash , and Merge Join usage during Optimiser phase for parse tree & Benchmarking was originally published in Stackademic on Medium, where people are continuing the conversation by highlighting and responding to this story.
