# 23.4 — Association

## Association requirements

To qualify as an **association**, an object and another object must have the following relationship:

| Requirement | Description |
|-------------|-------------|
| **Otherwise unrelated** | The associated object is otherwise unrelated to the object |
| **Multiple ownership allowed** | The associated object can belong to more than one object at a time |
| **Unmanaged existence** | The associated object does NOT have its existence managed by the object |
| **Bidirectional possible** | The associated object may or may not know about the existence of the object |

Unlike composition or aggregation (which are part-whole relationships), in an **association**, the objects are **otherwise unrelated**. Associations can be **unidirectional or bidirectional**.

Association models a **"uses-a"** relationship.

## Real-life example: Doctor and Patient

- A doctor sees many patients; a patient sees many doctors
- Neither object's lifespan is tied to the other
- The doctor "uses" the patient (to earn income)
- The patient "uses" the doctor (for health purposes)

## Implementation

Associations are most often implemented using **pointers**:

```cpp
#include <functional> // reference_wrapper
#include <iostream>
#include <string>
#include <vector>

class Patient;  // Forward declaration

class Doctor
{
private:
    std::string m_name{};
    std::vector<std::reference_wrapper<const Patient>> m_patient{};

public:
    Doctor(std::string_view name) : m_name{ name } {}
    
    void addPatient(Patient& patient);
    friend std::ostream& operator<<(std::ostream& out, const Doctor& doctor);
    const std::string& getName() const { return m_name; }
};

class Patient
{
private:
    std::string m_name{};
    std::vector<std::reference_wrapper<const Doctor>> m_doctor{};
    
    void addDoctor(const Doctor& doctor) { m_doctor.push_back(doctor); }

public:
    Patient(std::string_view name) : m_name{ name } {}
    friend std::ostream& operator<<(std::ostream& out, const Patient& patient);
    const std::string& getName() const { return m_name; }
    
    friend void Doctor::addPatient(Patient& patient);
};

void Doctor::addPatient(Patient& patient)
{
    m_patient.push_back(patient);      // Doctor adds patient
    patient.addDoctor(*this);          // Patient adds doctor (bidirectional)
}
```

> **Tip**: Avoid bidirectional associations if unidirectional will do - they add complexity.

## Reflexive association

Objects may have a relationship with other objects of the **same type**:

```cpp
class Course
{
private:
    std::string m_name{};
    const Course* m_prerequisite{};  // Course points to another Course

public:
    Course(std::string_view name, const Course* prerequisite = nullptr)
        : m_name{ name }, m_prerequisite{ prerequisite } {}
};
```

## Indirect associations

Associations don't require direct pointers/references. You can link objects by **ID**:

```cpp
class Car
{
private:
    std::string m_name{};
    int m_id{};

public:
    Car(std::string_view name, int id) : m_name{ name }, m_id{ id } {}
    const std::string& getName() const { return m_name; }
    int getId() const { return m_id; }
};

class Driver
{
private:
    std::string m_name{};
    int m_carId{};  // Associated by ID, not pointer

public:
    Driver(std::string_view name, int carId) : m_name{ name }, m_carId{ carId } {}
    int getCarId() const { return m_carId; }
};

// Get car from lot by ID
Car* car = CarLot::getCar(driver.getCarId());
```

### Advantages of ID-based associations:
- Can reference objects not currently in memory
- More compact (8-bit/16-bit ID vs 4-8 byte pointer)

## Comparison Table

| Property | Composition | Aggregation | Association |
|----------|-------------|-------------|-------------|
| **Relationship type** | Whole/part | Whole/part | Otherwise unrelated |
| **Multiple owners** | No | Yes | Yes |
| **Existence managed** | Yes | No | No |
| **Directionality** | Unidirectional | Unidirectional | Uni- or bidirectional |
| **Relationship verb** | Part-of | Has-a | Uses-a |

## Summary

- **Association** = "uses-a" relationship between unrelated objects
- More flexible than composition/aggregation
- Can be bidirectional
- Often implemented with pointers or indirect means (IDs)
- Avoid bidirectional when unidirectional suffices
