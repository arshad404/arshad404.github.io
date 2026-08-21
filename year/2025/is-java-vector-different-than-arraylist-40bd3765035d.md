# Java Vector vs ArrayList: Thread Safety and Performance

#synchronization #java-collection #vector #java #benchmark

## Benchmarking Vector and ArrayList

When working with Java collections, one common point of confusion is the difference between ArrayList and Vector. At first glance, they seem nearly identical—both are backed by dynamic arrays, offer random access via index, and implement the same fundamental methods like add(), get(), remove(), and size(). So naturally, the question arises:

If they’re so similar, why does Java even have both?The answer lies in concurrency.

## Vector is Synchronized — ArrayList is Not

The key distinction is that Vector is synchronized, meaning all of its methods are thread-safe by default. This makes it suitable for multi-threaded environments where concurrent access to the list may occur.

On the other hand, ArrayList is not synchronized, making it faster in single-threaded scenarios. If you need synchronization with ArrayList, you'll have to manually wrap it using:

```List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
```

## Benchmarking: Vector vs ArrayList

To better understand the performance impact of synchronization, I ran a simple benchmark using two threads writing concurrently to both a Vector and an ArrayList.

Here’s the Java code I used:

```package org.example.collections;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class VectorVsArrayList {
    public static void main(String[] args) throws InterruptedException {
        int N = 100_000;

        // Testing with ArrayList (Not Thread-Safe)
        List<Integer> arrayList = new ArrayList<>();
        long arrayListTime = measureConcurrentWriteTime(arrayList, N);
        System.out.println("ArrayList Size: " + arrayList.size() + " | Time taken: " + arrayListTime + " ms");

        // Testing with Vector (Thread-Safe)
        List<Integer> vector = new Vector<>();
        long vectorTime = measureConcurrentWriteTime(vector, N);
        System.out.println("Vector Size: " + vector.size() + " | Time taken: " + vectorTime + " ms");
    }

    private static long measureConcurrentWriteTime(List<Integer> list, int N) throws InterruptedException {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < N; i++) {
                list.add(i);
            }
        });

        Thread t2 = new Thread(() -> {
            for (int i = N; i < 2 * N; i++) {
                list.add(i);
            }
        });

        long start = System.currentTimeMillis();
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        long end = System.currentTimeMillis();

        return end - start;
    }
}
```

And this is the output of running the above program

```ArrayList Size: 138332 | Time taken: 16 ms
Vector Size: 200000 | Time taken: 19 ms
```

In this test, the ArrayList didn’t throw errors, but the final size was incorrect due to concurrent modifications. Meanwhile, the Vector maintained consistency at the cost of performance.

tl:dr;

- Vector keeps internal consistency but not atomicity of operations unless synchronized externally.

- ArrayList isn't thread-safe at all — expect corrupted data if used without external synchronization.

## A message from our Founder

Hey, Sunil here. I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 200k supporters? We do not get paid by Medium!

If you want to show some love, please take a moment to follow me on LinkedIn, TikTok and Instagram. And before you go, don’t forget to clap and follow the writer️!

Is Java Vector different than ArrayList? was originally published in Stackademic on Medium, where people are continuing the conversation by highlighting and responding to this story.
