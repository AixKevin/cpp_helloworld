# 23.x — Chapter 23 summary and quiz

## Chapter Summary

### Object Relationships Overview

This chapter explored different kinds of relationships between objects:

| Relationship | Models | Managed Lifetime | Multiple Owners | Directionality |
|--------------|--------|------------------|-----------------|----------------|
| **Composition** | Part-of | Yes | No | Unidirectional |
| **Aggregation** | Has-a | No | Yes | Unidirectional |
| **Association** | Uses-a | No | Yes | Uni- or Bidirectional |
| **Dependency** | Depends-on | No | Yes | Unidirectional |

### Composition

**Composition** exists when a member has a **part-of** relationship with the class:
- Part can only belong to one object at a time
- Class manages existence of parts
- Part doesn't know about the object
- Implemented via normal member variables or managed pointers
- **"If you can use composition, you should"**

### Aggregation

**Aggregation** exists when a class has a **has-a** relationship:
- Part can belong to multiple objects
- Class does NOT manage existence of parts
- Part doesn't know about the object
- Implemented via pointer or reference members
- Use `std::reference_wrapper` for containers of references

### Association

**Association** is a looser relationship where the class **uses-an** unrelated object:
- Associated object is otherwise unrelated
- Can belong to multiple objects
- Existence not managed
- May be uni- or bidirectional
- Implemented via pointers, references, or indirect means (IDs)

### Dependency

**Dependency** occurs when one object invokes another's functionality:
- Weaker than association
- Dependent object typically not a member
- Instantiated as needed or passed as parameter
- Always unidirectional

### Container Classes

**Container classes** hold and organize multiple instances of another type:
- **Value containers**: Store copies (composition)
- **Reference containers**: Store pointers/references (aggregation)
- Implement standard operations: create, insert, remove, size, clear, access, sort
- Prefer standard library containers when available

### std::initializer_list

Allows list initialization for custom classes:
- Lives in `<initializer_list>` header
- Lightweight view, passed by value
- List initialization **favors list constructors**
- Provide list assignment if you provide list construction
- Adding list constructors to existing classes can break code

## Comparison Table

| Property | Composition | Aggregation | Association | Dependency |
|----------|-------------|-------------|-------------|------------|
| **Relationship type** | Whole/part | Whole/part | Otherwise unrelated | Otherwise unrelated |
| **Multiple owners** | No | Yes | Yes | Yes |
| **Existence managed** | Yes | No | No | No |
| **Directionality** | Unidirectional | Unidirectional | Uni/bidirectional | Unidirectional |
| **Relationship verb** | Part-of | Has-a | Uses-a | Depends-on |

## Quiz Answers

**1a) Animal with type and name**: Composition -- type and name don't have use outside Animal

**1b) Text editor with save(File)**: Dependency -- editor uses File for saving task

**1c) Adventurer carrying Items**: Association -- not whole-part, Adventurer uses Items

**1d) Player prays at Shrine**: Dependency -- temporary use, no long-term association

**1e) Computer with CPU**: Aggregation -- Computer has CPU but doesn't manage existence

**1f) Blacksmith with anvil**: Association -- uses anvil, no whole-part relationship

**2) Which relationship to favor**: **Composition** -- If you can design a class using composition, you should.
