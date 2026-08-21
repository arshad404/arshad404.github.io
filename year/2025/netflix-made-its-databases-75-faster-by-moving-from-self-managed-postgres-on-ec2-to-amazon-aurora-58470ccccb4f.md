# Netflix made its databases 75% faster by moving from self-managed Postgres on EC2 to Amazon Aurora…

#aurora #aws #software-engineering #postgresql #data-engineering

## Netflix made its databases 75% faster by moving from self-managed Postgres on EC2 to Amazon Aurora, costs down by 28%

I recently read a LinkedIn post by Gaurav Sen featuring a blog on how Netflix increased its database performance by 75% and reduced costs by 28%.

### Blog Index

- Introduction

- Why Netflix Migrated to Aurora

- Why Aurora Was Chosen

- Performance Gains After Migration

- Understanding Aurora’s Architecture Advantage

- PostgreSQL vs Aurora: Double Buffering Explained

- Read Path Comparison: PostgreSQL vs Aurora

- Write Path Comparison: PostgreSQL vs Aurora

- Deep Dive: PostgreSQL Write Workflow (Step-by-Step with query)

I recently read a LinkedIn post by Gaurav Sen featuring a blog on how Netflix increased its database performance by 75% and reduced costs by 28%. Since I’m still new to Aurora and Postgres, it made me explore how this optimization was achieved. Here’s the main blog: https://aws.amazon.com/blogs/database/netflix-consolidates-relational-database-infrastructure-on-amazon-aurora-achieving-up-to-75-improved-performance/

## Here is the summary of the AWS Netflix blog:

### Why migration?

- Netflix’s internal data-infrastructure team (the “ODS team”) moved from a self-managed, distributed PostgreSQL-compatible database (on EC2 instances) to the managed Aurora PostgreSQL service. Amazon Web Services, Inc.

- The reason: their prior setup had become unwieldy — requiring manual scaling, patching, maintenance, license costs, and fragmented tooling. Amazon Web Services, Inc.

- The migration was motivated by four evaluation criteria: developer productivity, operational efficiency, performance reliability, and scalability/cost. Amazon Web Services, Inc.

### Why Aurora was chosen

- Compatibility & Developer Familiarity: Aurora PostgreSQL is PostgreSQL-compatible, so engineers could reuse their existing knowledge and tooling, minimizing friction or code changes. Amazon Web Services, Inc.

- Performance & Architecture Gains: Aurora’s architecture decouples compute and storage, uses a log-based write system (instead of writing full data pages), and stores data redundantly across multiple availability zones. This enables high write throughput and low latency. Amazon Web Services, Inc.+1

- Operational Simplicity: As a fully managed service, Aurora eliminates manual tasks like scaling storage, fail-over setup, backups, patching — reducing maintenance overhead significantly. Amazon Web Services, Inc.

- Cost Efficiency & Scalability: With a pay-as-you-go billing model, Netflix realized ~ 28% cost savings compared to their previous license-based model. Aurora also supports auto-scaling storage (up to 256 TB) and automated backups. Amazon Web Services, Inc.

### After migrating:

- Overall database performance improved up to 75% across Netflix’s internal relational workloads. Amazon Web Services, Inc.

- For example, the microservice Spinnaker (Front50) saw ~50% reduction in average latency, and a ~70% reduction in maximum latency — improving responsiveness and reducing latency spikes. Amazon Web Services, Inc.

- Another internal service, Policy Engine, experienced major latency reductions (e.g. one endpoint’s response time dropped from ~26.72 ms to ~6.51 ms), along with more stable and predictable performance. Amazon Web Services, Inc.

- Operationally, Netflix eliminated most of the overhead involved in managing their own database fleet — giving engineers back time to focus on building features rather than database maintenance. Amazon Web Services, Inc.

After reading the blog, I understood why the migration taken place and what are the benefits of the migration. But the question in my mind is still the same, what is special in the Aurora which outperform the Postgres in terms of latency because I understand the point of maintainability here but for performance I need to read more.

### Why Aurora is Faster: Shared Memory vs OS Page Cache (Double Buffering)

### How normal PostgreSQL works (EC2 self-managed)

When PostgreSQL runs on a Linux server, it always uses two layers of caching:

### 1. PostgreSQL Shared Buffers

- A fixed chunk of RAM inside Postgres.

- Postgres copies data from disk into this area.

- All queries read/write through this buffer.

### 2. OS Page Cache

- Linux also caches the same data in RAM.

- So every read/write goes like this:

```Disk → OS Page Cache → Postgres Shared Buffers → Query
```

This is called double buffering because the same data is stored twice in RAM.

### Problems with double buffering

- Wasted memory If you have 64 GB RAM, maybe only ~20–25 GB is usable by Postgres shared buffers. The OS also keeps another copy → effective usable memory is reduced.

- More copies → more CPU + more latency Every read/write moves through two layers.

- Under load → latency spikes OS decides when to flush dirty pages → sudden I/O spikes → unpredictable performance.

### How Amazon Aurora is different

Aurora removes the OS page cache completely. It uses its own distributed storage engine, so data flows:

```Aurora Storage → Shared Memory (Buffer Cache) → Query
```

Only ONE buffer layer. No OS cache. No double buffering.

### Benefits

- ~75% of RAM can be used directly as Postgres buffer cache (In normal Postgres, you can safely use only ~25–30%)

- No duplicate copies → more effective RAM

- Lower latency → fewer memory copies

- Writes are much faster, because Aurora writes redo logs directly to storage nodes instead of using Linux flush mechanism.

For more clarity we can see the read flow of both the databases

### Postgres read:

```Client
   │
   ▼
Check Shared Buffers
   │
   ├── Hit → return directly
   │
   └── Miss
          │
          ▼
      OS Page Cache
          │
          ├── Hit → copy into shared buffer → return
          │
          └── Miss 
                 │
                 ▼
             Read from Disk (EBS)
```

### Aurora read:

```Client
   │
   ▼
Check Shared Buffers
   │
   ├── Hit → return
   │
   └── Miss
          │
          ▼
   Fetch Page from Aurora Storage Nodes
          │   (distributed, SSD-backed)
          ▼
Return and cache in Shared Buffers
```

### Postgres write

```Modify Page
Write WAL
Write Data Page (dirty page)
fsync
checkpoint
OS flush
```

### Aurora write

```Modify Page
Generate Redo Only
Send Redo
Quorum Commit
(NO data page writes)
(NO checkpoints)
```

Still I want to go in depth with query example for the postgres write pattern, so here is what I have read and summarising it here

### Query from interface

```UPDATE users SET age = 30 WHERE id = 1001;
```

### STEP 1 — Load the page into Shared Buffers

Postgres finds which 8KB page contains user id = 1001.

If not already in RAM:

```Disk → OS Page Cache → Shared Buffers
```

Now Postgres has the page on its desk.

### STEP 2 — Modify the page in Shared Buffers

It updates the row inside the 8KB page. The page becomes a dirty page:

```[ Shared Buffers ]
   ↓
  Page marked “Dirty”
```

Nothing has been written to disk yet. Postgres is only working in memory.

### STEP 3 — Write the action to WAL first (Write-Ahead Log)

Postgres now writes:

```"Row X changed from Y → Z"
```

into the WAL Buffer. Once the WAL buffer is full or a commit happens, Postgres flushes it:

```WAL Buffer → WAL File on Disk → fsync()
```

This is the ONLY data guaranteed durable at COMMIT time. Not the updated row — only the redo log. This makes Postgres crash-safe.

### STEP 4 — Return success to client

Yes — even though data itself is NOT written to disk yet.

The client thinks the update is done, but the real data is still:

- in RAM

- dirty

- not persisted

Why is this allowed?

- Because WAL is durable, and WAL can rebuild the data.

### STEP 5 — Later… Background Writer writes dirty pages

A background process periodically chooses dirty pages:

```Shared Buffers → OS Page Cache → Disk
```

This is a slow path because:

- must write full 8KB page

- must go through OS

- must wait for disk scheduling

- must compete with other I/O

But Postgres delays this as long as possible to avoid slowdown.

### STEP 6 — Checkpointer forces all dirty pages to disk

Periodically:

```Checkpoint = full flush of all dirty pages to disk
```

This ensures recovery time stays small (less WAL to replay).

Checkpoints create:

- write bursts

- latency spikes

- “check pointer doing full page write” warnings

This is one of the biggest reasons Aurora was invented.

### PostgreSQL Write Path

```1. Modify page in Shared Buffers
        │
        ▼
2. Generate WAL records
        │
        ▼
3. WAL Buffer → WAL file → fsync  (client sees COMMIT)
        │
        ▼
4. Dirty Pages wait in Shared Buffers
        │
        ▼
5. Background Writer writes pages → OS Page Cache
        │
        ▼
6. OS flush writes page → Disk (EBS)
        │
        ▼
7. Checkpoint forces all writes periodically
```

Now after reading the full write path of the Postgres, I am now able to understand the blog. Thanks for reading, stay hydrated, take care.
