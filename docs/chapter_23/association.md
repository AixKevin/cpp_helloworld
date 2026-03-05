# 23.4 — 关联

23.4 — 关联
Alex
2016 年 8 月 19 日，下午 5:18 （太平洋夏令时）
2023 年 12 月 7 日
在前面的两节课中，我们学习了两种类型的对象组合：复合和聚合。对象组合用于建模复杂对象由一个或多个简单对象（部分）构建的关系。
在本节课中，我们将探讨两种原本不相关的对象之间的一种较弱的关系，称为关联。与对象组合关系不同，在关联中，不存在隐含的整体/部分关系。
关联
要符合
关联
的条件，一个对象和另一个对象必须具有以下关系：
关联对象（成员）与对象（类）原本不相关
关联对象（成员）可以同时属于多个对象（类）
关联对象（成员）的生命周期不受对象（类）管理
关联对象（成员）可能知道也可能不知道对象（类）的存在
与复合或聚合不同，在复合或聚合中，部分是整体对象的一部分，而在关联中，关联对象与对象原本不相关。就像聚合一样，关联对象可以同时属于多个对象，并且不受这些对象的管理。然而，与聚合不同的是，聚合中的关系总是单向的，而在关联中，关系可以是单向的，也可以是双向的（两个对象彼此都知晓）。
医生和患者之间的关系是关联的一个很好的例子。医生与他的患者显然有关系，但从概念上讲，它不是部分/整体（对象组合）关系。医生一天可以看很多患者，患者也可以看很多医生（也许他们想要第二种意见，或者他们正在看不同类型的医生）。这两个对象的生命周期互不关联。
我们可以说关联建模为“使用（uses-a）”关系。医生“使用”患者（以赚取收入）。患者使用医生（出于他们需要的任何健康目的）。
实现关联
由于关联是一种广泛的关系类型，因此可以通过多种不同的方式实现。然而，通常情况下，关联是使用指针实现的，其中对象指向关联对象。
在这个例子中，我们将实现一个双向的医生/患者关系，因为医生了解他们的患者以及反之亦然是很合理的。
#include <functional> // reference_wrapper
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

// Since Doctor and Patient have a circular dependency, we're going to forward declare Patient
class Patient;

class Doctor
{
private:
	std::string m_name{};
	std::vector<std::reference_wrapper<const Patient>> m_patient{};

public:
	Doctor(std::string_view name) :
		m_name{ name }
	{
	}

	void addPatient(Patient& patient);
	
	// We'll implement this function below Patient since we need Patient to be defined at that point
	friend std::ostream& operator<<(std::ostream& out, const Doctor& doctor);

	const std::string& getName() const { return m_name; }
};

class Patient
{
private:
	std::string m_name{};
	std::vector<std::reference_wrapper<const Doctor>> m_doctor{}; // so that we can use it here

	// We're going to make addDoctor private because we don't want the public to use it.
	// They should use Doctor::addPatient() instead, which is publicly exposed
	void addDoctor(const Doctor& doctor)
	{
		m_doctor.push_back(doctor);
	}

public:
	Patient(std::string_view name)
		: m_name{ name }
	{
	}

	// We'll implement this function below to parallel operator<<(std::ostream&, const Doctor&)
	friend std::ostream& operator<<(std::ostream& out, const Patient& patient);

	const std::string& getName() const { return m_name; }

	// We'll friend Doctor::addPatient() so it can access the private function Patient::addDoctor()
	friend void Doctor::addPatient(Patient& patient);
};

void Doctor::addPatient(Patient& patient)
{
	// Our doctor will add this patient
	m_patient.push_back(patient);

	// and the patient will also add this doctor
	patient.addDoctor(*this);
}

std::ostream& operator<<(std::ostream& out, const Doctor& doctor)
{
	if (doctor.m_patient.empty())
	{
		out << doctor.m_name << " has no patients right now";
		return out;
	}

	out << doctor.m_name << " is seeing patients: ";
	for (const auto& patient : doctor.m_patient)
		out << patient.get().getName() << ' ';

	return out;
}

std::ostream& operator<<(std::ostream& out, const Patient& patient)
{
	if (patient.m_doctor.empty())
	{
		out << patient.getName() << " has no doctors right now";
		return out;
	}

	out << patient.m_name << " is seeing doctors: ";
	for (const auto& doctor : patient.m_doctor)
		out << doctor.get().getName() << ' ';

	return out;
}

int main()
{
	// Create a Patient outside the scope of the Doctor
	Patient dave{ "Dave" };
	Patient frank{ "Frank" };
	Patient betsy{ "Betsy" };

	Doctor james{ "James" };
	Doctor scott{ "Scott" };

	james.addPatient(dave);

	scott.addPatient(dave);
	scott.addPatient(betsy);

	std::cout << james << '\n';
	std::cout << scott << '\n';
	std::cout << dave << '\n';
	std::cout << frank << '\n';
	std::cout << betsy << '\n';

	return 0;
}
这会打印
James is seeing patients: Dave
Scott is seeing patients: Dave Betsy
Dave is seeing doctors: James Scott
Frank has no doctors right now
Betsy is seeing doctors: Scott
一般来说，如果单向关联可以满足需求，则应避免双向关联，因为它们会增加复杂性，并且更容易出错。
自关联
有时对象可能与相同类型的其他对象存在关系。这称为
自关联
。自关联的一个很好的例子是大学课程及其先决条件（也都是大学课程）之间的关系。
考虑简化情况，即一门课程只能有一个先决条件。我们可以这样做：
#include <string>
#include <string_view>

class Course
{
private:
    std::string m_name{};
    const Course* m_prerequisite{};

public:
    Course(std::string_view name, const Course* prerequisite = nullptr):
        m_name{ name }, m_prerequisite{ prerequisite }
    {
    }

};
这可能导致一系列关联（一门课程有一个先决条件，该先决条件又有一个先决条件，等等…）
关联可以是间接的
在之前的所有情况下，我们都使用了指针或引用来直接链接对象。然而，在关联中，这不是严格必需的。任何允许您将两个对象链接在一起的数据都足够了。在下面的示例中，我们展示了 Driver 类如何与 Car 建立单向关联，而无需实际包含 Car 指针或引用成员：
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
	std::string m_name{};
	int m_id{};

public:
	Car(std::string_view name, int id)
		: m_name{ name }, m_id{ id }
	{
	}

	const std::string& getName() const { return m_name; }
	int getId() const { return m_id; }
};

// Our CarLot is essentially just a static array of Cars and a lookup function to retrieve them.
// Because it's static, we don't need to allocate an object of type CarLot to use it
namespace CarLot
{
    Car carLot[4] { { "Prius", 4 }, { "Corolla", 17 }, { "Accord", 84 }, { "Matrix", 62 } };

	Car* getCar(int id)
	{
		for (auto& car : carLot)
        {
			if (car.getId() == id)
			{
				return &car;
			}
		}
		
		return nullptr;
	}
};

class Driver
{
private:
	std::string m_name{};
	int m_carId{}; // we're associated with the Car by ID rather than pointer

public:
	Driver(std::string_view name, int carId)
		: m_name{ name }, m_carId{ carId }
	{
	}

	const std::string& getName() const { return m_name; }
	int getCarId() const { return m_carId; }
};

int main()
{
	Driver d{ "Franz", 17 }; // Franz is driving the car with ID 17

	Car* car{ CarLot::getCar(d.getCarId()) }; // Get that car from the car lot
	
	if (car)
		std::cout << d.getName() << " is driving a " << car->getName() << '\n';
	else
		std::cout << d.getName() << " couldn't find his car\n";

	return 0;
}
在上面的例子中，我们有一个 CarLot 持有我们的汽车。需要汽车的 Driver 没有指向其 Car 的指针——相反，他拥有汽车的 ID，我们可以使用它在需要时从 CarLot 中获取 Car。
在这个特定的例子中，这样做有点傻，因为从 CarLot 中取出 Car 需要低效的查找（连接两者的指针要快得多）。然而，通过唯一 ID 而不是指针引用事物有其优点。例如，您可以引用当前不在内存中的事物（它们可能在文件中，或在数据库中，可以按需加载）。此外，指针可能占用 4 或 8 字节——如果空间非常宝贵且唯一对象的数量相当少，通过 8 位或 16 位整数引用它们可以节省大量内存。
复合 vs 聚合 vs 关联 总结
下面是一个总结表，帮助您记住复合、聚合和关联之间的区别：
属性
组合
聚合
关联
关系类型
整体/部分
整体/部分
原本不相关
成员可以属于多个类
否
是
是
成员的生命周期由类管理
是
否
否
方向性
单向
单向
单向或双向
关系动词
是…的一部分
拥有
使用
下一课
23.5
依赖关系
返回目录
上一课
23.3
聚合