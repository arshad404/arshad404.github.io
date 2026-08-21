# ArrayDeque vs Stack in Java: Choosing the Right Tool

#concurrency #arraydeque #java #stack #java-collection

## Choosing Between ArrayDeque and Stack

### Benchmark results: 65ms vs 100ms

Photo by Tracy Adams on UnsplashJava provides multiple ways to implement a stack, and two popular choices are Stack and ArrayDeque. At first glance, both support standard stack operations like push(), pop(), and peek(), but they differ significantly under the hood.

### Stack (Legacy and Synchronized)

Stack is a legacy class that extends Vector, which means it's synchronized by default. While this was helpful in older Java versions, it introduces performance overhead in single-threaded environments.

Hierarchy of Stack:

```
java.lang.Object
  ↳ java.util.AbstractCollection
    ↳ java.util.Vector
      ↳ java.util.Stack
```

### ArrayDeque (Modern and Efficient)

ArrayDeque is part of the Java Collections Framework and provides a non-synchronized, resizable array-based implementation of a double-ended queue (deque). When used as a stack (via push(), pop()), it is faster and more memory efficient than Stack.

Hierarchy of ArrayDeque:

```
java.lang.Object
  ↳ java.util.AbstractCollection
    ↳ java.util.AbstractQueue
      ↳ java.util.ArrayDeque
```

### Which Should You Use?

Unless you need built-in synchronization (which is rare and better handled by external mechanisms like Collections.synchronizedList() or ConcurrentLinkedDeque), prefer ArrayDeque. It is the recommended stack implementation in modern Java applications due to its performance benefits and cleaner API.

As you know I love the benchmarking 😂 so here is the codebase for the same

```package org.example.collections;


import java.util.ArrayDeque;
import java.util.Stack;

public class StackVsArrayDeque {

    private static final int NUM_ELEMENTS = 1_000_000;

    public static void main(String[] args) {
        benchmarkStack();
        benchmarkArrayDeque();
    }

    private static void benchmarkStack() {
        Stack<Integer> stack = new Stack<>();

        long startTime = System.nanoTime();
        for (int i = 0; i < NUM_ELEMENTS; i++) {
            stack.push(i); // O(1) amortized
        }

        for (int i = 0; i < NUM_ELEMENTS; i++) {
            stack.peek(); // O(1)
        }

        for (int i = 0; i < NUM_ELEMENTS; i++) {
            stack.pop(); // O(1)
        }
        long endTime = System.nanoTime();

        System.out.println("Time taken by Stack      : " + ((endTime - startTime) / 1_000_000) + " ms");
    }

    private static void benchmarkArrayDeque() {
        ArrayDeque<Integer> deque = new ArrayDeque<>();

        long startTime = System.nanoTime();
        for (int i = 0; i < NUM_ELEMENTS; i++) {
            deque.push(i); // O(1) amortized
        }

        for (int i = 0; i < NUM_ELEMENTS; i++) {
            deque.peek(); // O(1)
        }

        for (int i = 0; i < NUM_ELEMENTS; i++) {
            deque.pop(); // O(1)
        }
        long endTime = System.nanoTime();

        System.out.println("Time taken by ArrayDeque : " + ((endTime - startTime) / 1_000_000) + " ms");
    }
}
```

Results are really surprising, I was not expecting this much honestly

```Time taken by Stack      : 100 ms
Time taken by ArrayDeque : 65 ms
```

## A message from our Founder

Hey, Sunil here. I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 200k supporters? We do not get paid by Medium!

If you want to show some love, please take a moment to follow me on LinkedIn, TikTok and Instagram. And before you go, don’t forget to clap and follow the writer️!
