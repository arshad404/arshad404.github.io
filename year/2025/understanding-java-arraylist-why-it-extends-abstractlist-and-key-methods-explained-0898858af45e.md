---
published: 2025-07-28T18:49:07Z
source: medium
medium_url: https://arshad404.medium.com/understanding-java-arraylist-why-it-extends-abstractlist-and-key-methods-explained-0898858af45e
---

# Understanding Java ArrayList: AbstractList and Core Methods

#java-collection #interview #java #problem-solving #data-structures

## Why ArrayList Extends AbstractList

### What AbstractList Provides

In Java, the ArrayList class extends AbstractList, which in turn implements the List interface. This might raise a common question for many developers:

Why not directly implement List in ArrayList? Why bring AbstractList into the picture?

The answer lies in code reuse and maintainability.

### Role of AbstractList

AbstractList is an abstract class that provides skeletal implementations of the List interface methods such as:

- get(int index)

- size()

- isEmpty()

- iterator()

- toString()

These implementations are often generic and reusable, saving every List implementation (like ArrayList, LinkedList, etc.) from having to re-implement basic functionalities.

By extending AbstractList, the ArrayList class inherits:

- Default behavior for many List operations

- The freedom to override and optimize only where necessary (e.g., random access in ArrayList is O(1))

### Benefit for Developers

For those doing problem solving, methods that matter most are:

- get(index) – O(1)

- size() – O(1)

- add(element) – Amortized O(1)

- remove(index) – O(n)

- set(index, element) – O(1)

These methods are often provided either by AbstractList or overridden in ArrayList for performance.

### TL;DR

ArrayList extends AbstractList to:

- Reuse common logic for List operations

- Avoid re-writing boilerplate code

- Provide a clean and efficient implementation for developers

This design pattern is a great example of the Template Method Pattern in Java’s Collections Framework.

### Example

```package org.example.collections;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

class Person {
    Person(String name, Integer age) {
        this.name = name;
        this.age = age;
    }

    public String name;
    public Integer age;
}

public class ArrayListCollection {

    public static void main(String[] args) {
        // Initialise — O(1) per add, O(n) total if resizing needed
        ArrayList<Integer> arr = new ArrayList<>();
        arr.add(4); // O(1) amortized
        arr.add(2); // O(1) amortized
        arr.add(3); // O(1) amortized

        // size — O(1)
        int sz = arr.size();

        // sort — O(n log n)
        Collections.sort(arr);

        // get — O(1) per access
        for(int i = 0; i < sz; i++) {
            System.out.println(arr.get(i)); // O(1) per access
        }

        // fill — O(n)
        Collections.fill(arr, -1); // Replaces each element

        // remove — O(n) worst-case (due to shifting)
        arr.remove(1); // Removes index 1, shifts elements to the left

        // get — O(1) per access
        for(int i = 0; i < sz; i++) {
            System.out.println(arr.get(i)); // O(1)
        }

        Person person1 = new Person("harry", 20);
        Person person2 = new Person("james", 24);

        // add — O(1) amortized
        ArrayList<Person> personArrayList = new ArrayList<>();
        personArrayList.add(person2); // O(1)
        personArrayList.add(person1); // O(1)

        // iteration — O(n)
        for(Person person: personArrayList) {
            System.out.println(person.name); // O(1)
        }

        // sort using Comparator — O(n log n)
        personArrayList.sort(Comparator.comparingInt(p -> p.age)); // O(n log n)

        // iteration — O(n)
        for(Person person: personArrayList) {
            System.out.println(person.name); // O(1)
        }
    }
}
```

### Summary on operations time complexity:

source: chatgpt.com

## A message from our Founder

Hey, Sunil here. I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 200k supporters? We do not get paid by Medium!

If you want to show some love, please take a moment to follow me on LinkedIn, TikTok and Instagram. And before you go, don’t forget to clap and follow the writer️!

Understanding Java ArrayList was originally published in Stackademic on Medium, where people are continuing the conversation by highlighting and responding to this story.
