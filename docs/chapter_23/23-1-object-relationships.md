# 23.1 — Object relationships

Life is full of recurring patterns, relationships, and hierarchies between objects. By exploring and understanding these, we can gain insight into how real-life objects behave, enhancing our understanding of those objects.

## Relationships between objects

There are many different kinds of relationships two objects may have in real-life, and we use specific "relation type" words to describe these relationships:

| Relationship | Example | C++ Analogy |
|--------------|---------|-------------|
| **is-a** | A square "is-a" shape | Inheritance |
| **has-a** | A car "has-a" steering wheel | Composition/Aggregation |
| **uses-a** | A programmer "uses-a" keyboard | Association |
| **depends-on** | A flower "depends-on" a bee | Dependency |
| **member-of** | A student is a "member-of" a class | Container classes |
| **part-of** | Your brain is "part-of" you | Composition |

## Chapter overview

In this chapter, we'll explore the nuances of the relation types:
- **part-of** (Composition)
- **has-a** (Aggregation)
- **uses-a** (Association)
- **depends-on** (Dependency)
- **member-of** (Container classes)

Then we'll devote the following two chapters to exploring **"is-a"** relationships, via C++'s inheritance model and virtual functions.

## Summary

- Object relationships mirror real-life relationships
- Different relationship types have different semantics and implementations
- Understanding these relationships helps write better, more extensible code
- This chapter covers composition, aggregation, association, and dependency
- Chapters 24-25 cover inheritance ("is-a" relationships)
