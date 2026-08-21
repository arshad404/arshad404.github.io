# BM25: How Search Engines Rank Relevant Results

#mathematics #ai #coding #search-engines #database

When you search for something on Google or Amazon, how does the system decide which result is more relevant? One of the most popular and powerful algorithms used to rank documents based on a query is BM25 (Best Matching 25). It’s a probabilistic-based ranking function that plays a key role in modern Information Retrieval (IR) systems, including Elasticsearch, Lucene, and Solr.

BM25 is a ranking function that scores how well a document matches a search query. It builds on TF-IDF (Term Frequency–Inverse Document Frequency) and improves it by normalizing term frequency and accounting for document length.

The core idea is:

A term is more important if it appears frequently in a document but rarely in the overall corpus. However, longer documents tend to repeat terms more often, so they need to be normalized.BM25 Formula

- f(q, D): frequency of term q in document D.

- |D|: length of the document D (number of terms).

- avgdl: average document length in the entire collection.

- k: saturation parameter (controls term frequency scaling, usually 1.2 to 2.0).

- b: length normalization parameter (usually 0.75).

- IDF(q): inverse document frequency of the term q.

## 🧠 Intuition Behind Each Term

### IDF (Inverse Document Frequency)

This helps in boost rare terms.

IDF formula

- N: total number of documents.

- df(t): number of documents containing term t.

🔎 Rare terms = higher IDF = more impactful

## What Do Parameters k1 and b Do?

### k1: Term Frequency Saturation

- Controls how much weight you give to term frequency.

- Think of it as a throttle: how quickly extra occurrences of a word stop adding value.

- When k1 = 0, term frequency is ignored.

- Higher k1 = more weight for repeating the same word.

- Lower k1 = term frequency helps less after a few times.

Common default: k1 = 1.2 to 2.0

### b: Length Normalization Factor

- Controls how much the length of the document affects the score.

- Short docs are often better matches — they’re more focused.

- But if a doc is too long, matches get diluted.

- Controls how much to penalize longer documents.

- b = 0: no normalization (document length ignored)

- b = 1: full normalization based on length

Common default: b = 0.75Enough theory I guess, its code time. Lets see how the values calculated using a simple go program.

```package main

import (
 "fmt"
 "log"
 "math"
)

// Document struct represents a simple document
type Document struct {
 ID     string         // Unique ID for the document
 Words  []string       // Tokenized list of words
 TF     map[string]int // Term frequency map for each word
 Length int            // Total number of words in the document
}

func main() {
 // Single query term for simplicity
 queryTerm := "iphone"

 // BM25 parameters:
 // k1 controls term frequency saturation: higher = more sensitive to repetition
 // b controls length normalization: 0 = no length penalty, 1 = full normalization
 k1 := 1.5
 b := 0.75

 // Sample corpus of 3 documents (tokenized)
 docs := []Document{
  {ID: "D1", Words: []string{"apple", "iphone", "15", "pro", "max"}},
  {ID: "D2", Words: []string{"buy", "iphone", "iphone", "iphone", "apple", "iphone"}},
  {ID: "D3", Words: []string{"this", "is", "an", "iphone", "review", "iphone", "iphone", "iphone", "iphone", "iphone", "iphone"}},
 }

 // Step 1: Preprocess documents
 // - Calculate term frequencies for each document
 // - Track document lengths
 // - Compute document frequency (df) for the query term
 totalLength := 0
 df := 0 // Number of documents containing the query term

 for i := range docs {
  docs[i].TF = make(map[string]int)
  for _, word := range docs[i].Words {
   docs[i].TF[word]++
  }
  docs[i].Length = len(docs[i].Words)
  totalLength += docs[i].Length

  if docs[i].TF[queryTerm] > 0 {
   df++
  }
 }

 N := len(docs)                             // Total number of documents
 avgdl := float64(totalLength) / float64(N) // Average document length

 fmt.Printf("🔢 Total Documents (N): %d\n", N)
 fmt.Printf("📄 Documents with '%s' (df): %d\n", queryTerm, df)
 fmt.Printf("📏 Average Document Length (avgdl): %.2f\n\n", avgdl)

 // Step 2: Compute IDF
 // BM25 uses smoothed IDF:
 // IDF(t) = log((N - df + 0.5) / (df + 0.5) + 1)
 idf := math.Log((float64(N)-float64(df)+0.5)/(float64(df)+0.5) + 1)

 fmt.Printf("📘 IDF('%s') = %.4f (log-smoothing applied)\n\n", queryTerm, idf)

 // Step 3: Compute BM25 score for each document
 // Formula:
 // score(t, d) = IDF(t) * ((TF * (k1 + 1)) / (TF + k1 * (1 - b + b * (|d| / avgdl))))
 for _, doc := range docs {
  tf := float64(doc.TF[queryTerm])
  docLen := float64(doc.Length)

  // Compute BM25 numerator: TF * (k1 + 1)
  numerator := tf * (k1 + 1)

  // Compute BM25 denominator: TF + k1 * (1 - b + b * (|d| / avgdl))
  lengthNormalization := 1 - b + b*(docLen/avgdl)
  denominator := tf + k1*lengthNormalization

  if denominator == 0 {
   log.Fatalf("Denominator is zero for document %s (likely a bug)", doc.ID)
  }

  bm25Score := idf * (numerator / denominator)

  // Print results
  fmt.Printf("📄 Document: %s\n", doc.ID)
  fmt.Printf("   🔁 Term Frequency (TF): %d\n", doc.TF[queryTerm])
  fmt.Printf("   📏 Length: %d\n", doc.Length)
  fmt.Printf("   📊 BM25 Score: %.4f\n\n", bm25Score)
 }
}
```

The output of the above codebase is

```🔢 Total Documents (N): 3
📄 Documents with 'iphone' (df): 3
📏 Average Document Length (avgdl): 7.33

📘 IDF('iphone') = 0.1335 (log-smoothing applied)

📄 Document: D1
   🔁 Term Frequency (TF): 1
   📏 Length: 5
   📊 BM25 Score: 0.1558

📄 Document: D2
   🔁 Term Frequency (TF): 4
   📏 Length: 6
   📊 BM25 Score: 0.2522

📄 Document: D3
   🔁 Term Frequency (TF): 7
   📏 Length: 11
   📊 BM25 Score: 0.2579
```

### Observation:

We have these three documents,

- D1: “apple”, “iphone”, “15”, “pro”, “max”

- D2: “buy”, “iphone”, “iphone”, “iphone”, “apple”, “iphone”

- D3: “this”, “is”, “an”, “iphone”, “review”, “iphone”, “iphone”, “iphone”, “iphone”, “iphone”, “iphone”

Notice that D3 contains the term “iphone” with a very high frequency. However, the BM25 score for this document doesn’t increase dramatically. This demonstrates one of the key strengths of the BM25 algorithm — its ability to saturate term frequency, preventing documents from being unfairly boosted just because a term appears many times.

## Thank you for being a part of the community

Before you go:

- Be sure to clap and follow the writer ️👏️️

- Follow us: X | LinkedIn | YouTube | Newsletter | Podcast | Twitch

- Start your own free AI-powered blog on Differ 🚀

- Join our content creators community on Discord 🧑🏻‍💻

- For more content, visit plainenglish.io + stackademic.com

What is BM25? The Ranking Formula Behind Search Engines was originally published in JavaScript in Plain English on Medium, where people are continuing the conversation by highlighting and responding to this story.
